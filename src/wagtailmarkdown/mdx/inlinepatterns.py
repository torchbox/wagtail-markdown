from django.apps import apps
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from markdown import Extension
from markdown.inlinepatterns import (
    IMAGE_LINK_RE,
    LINK_RE,
    ImageInlineProcessor,
    LinkInlineProcessor,
)
from wagtail.documents import get_document_model
from wagtail.images import get_image_model
from wagtail.images.exceptions import InvalidFilterSpecError
from wagtail.models import Page


def _options_to_dict(value: str) -> dict:
    """
    Takes a "key=value,key2=value2" string and converts it to a dict
    """
    if not value.strip():
        return {}

    _dict = {}
    for key_value_pair in value.split(","):
        try:
            key, val = key_value_pair.split("=", 1)
            if key.strip():
                _dict[key.strip()] = val.strip()
        except ValueError:
            pass

    return _dict


class ObjectLookupNegotiator:
    PAGE_LINK_PREFIX = "page:"
    DOCUMENT_LINK_PREFIX = "doc:"
    IMAGE_PREFIX = "image:"
    MEDIA_PREFIX = "media:"

    @staticmethod
    def retrieve_page(lookup_field_value):
        try:
            return Page.objects.get(pk=lookup_field_value)
        except (Page.DoesNotExist, Page.MultipleObjectsReturned):
            return None

    @staticmethod
    def retrieve_document(lookup_field_value):
        try:
            return get_document_model().objects.get(pk=lookup_field_value)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None

    @staticmethod
    def retrieve_image(lookup_field_value):
        try:
            return get_image_model().objects.get(pk=lookup_field_value)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None

    @staticmethod
    def retrieve_wagtailmedia(lookup_field_value):
        if not apps.is_installed("wagtailmedia"):
            return None

        try:
            from wagtailmedia.models import get_media_model

            return get_media_model().objects.get(pk=lookup_field_value)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None

    @classmethod
    def retrieve(cls, url):
        pairs = (
            (cls.PAGE_LINK_PREFIX, cls.retrieve_page),
            (cls.DOCUMENT_LINK_PREFIX, cls.retrieve_document),
            (cls.IMAGE_PREFIX, cls.retrieve_image),
            (cls.MEDIA_PREFIX, cls.retrieve_wagtailmedia),
        )
        for prefix, object_retrieve_method in pairs:
            if url.startswith(prefix):
                return object_retrieve_method(url.replace(prefix, ""))


class ImageProcessor(ImageInlineProcessor):
    def __init__(self, object_lookup_negotiator, *args, **kwargs):
        self.object_lookup_negotiator = object_lookup_negotiator
        super().__init__(*args, **kwargs)

    def handleMatch(self, m, data):
        element, processed_m, index = super().handleMatch(m, data)
        if element is None:
            return element, processed_m, index

        pk, *opts_str = element.get("src", "").split(",", 1)
        image = self.object_lookup_negotiator.retrieve(pk)
        if image:
            opts = _options_to_dict(opts_str[0]) if opts_str else {}
            element.set("class", opts.get("class", "left"))

            rendition = self._get_rendition(image, opts.get("filter", "width-500"))
            element.set("src", rendition.url)
            element.set("width", str(rendition.width))
            element.set("height", str(rendition.height))
        return element, processed_m, index

    @staticmethod
    def _get_rendition(image, filter_spec):
        try:
            rendition = image.get_rendition(filter_spec)
        except InvalidFilterSpecError:
            rendition = image.get_rendition("width-500")

        return rendition


class LinkProcessor(LinkInlineProcessor):
    def __init__(self, object_lookup_negotiator, *args, **kwargs):
        self.object_lookup_negotiator = object_lookup_negotiator
        super().__init__(*args, **kwargs)

    def getLink(self, data, index):
        href, title, index, handled = super().getLink(data, index)
        target_object = self.object_lookup_negotiator.retrieve(href)
        if target_object:
            href = target_object.url

        return href, title, index, handled


class ImageExtension(Extension):
    def __init__(self, object_lookup_negotiator=None, **kwargs):
        self.object_lookup_negotiator = (
            object_lookup_negotiator or ObjectLookupNegotiator
        )
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            ImageProcessor(
                pattern=IMAGE_LINK_RE,
                md=md,
                object_lookup_negotiator=self.object_lookup_negotiator,
            ),
            "image_link",
            151,
        )


class LinkExtension(Extension):
    def __init__(self, object_lookup_negotiator=None, **kwargs):
        self.object_lookup_negotiator = (
            object_lookup_negotiator or ObjectLookupNegotiator
        )
        super().__init__(**kwargs)

    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            LinkProcessor(
                pattern=LINK_RE,
                md=md,
                object_lookup_negotiator=self.object_lookup_negotiator,
            ),
            "link",
            161,
        )
