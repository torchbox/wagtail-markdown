from django.apps import apps
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from wagtail.documents import get_document_model
from wagtail.images import get_image_model

from markdown import Extension
from markdown.inlinepatterns import (
    IMAGE_LINK_RE,
    LINK_RE,
    ImageInlineProcessor,
    LinkInlineProcessor,
)


try:
    from wagtail.models import Page
except ImportError:
    from wagtail.core.models import Page


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
        image = self.object_lookup_negotiator.retrieve(element.get("src", ""))
        if image:
            rendition = image.get_rendition("width-500")
            element.set("src", rendition.url)
            element.set("class", "left")
            element.set("width", str(rendition.width))
            element.set("height", str(rendition.height))
        return element, processed_m, index


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
