import re
import secrets
import xml.etree.ElementTree as etree

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from django.apps import apps
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from markdown import Extension, util
from markdown.inlinepatterns import (
    IMAGE_LINK_RE,
    LINK_RE,
    ImageInlineProcessor,
    LinkInlineProcessor,
    SimpleTagInlineProcessor,
)
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.documents import get_document_model
from wagtail.images import get_image_model
from wagtail.images.exceptions import InvalidFilterSpecError


if WAGTAIL_VERSION >= (8, 0):
    import swapper

    Page = swapper.load_model("wagtailcore", "Page")
else:
    from wagtail.models import Page


if TYPE_CHECKING:
    from django.db.models import Model
    from markdown import Markdown


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
            # ignore any key_value_pair that don't contain '='
            pass

    return _dict


class ObjectLookupNegotiator:
    PAGE_LINK_PREFIX = "page:"
    DOCUMENT_LINK_PREFIX = "doc:"
    IMAGE_PREFIX = "image:"
    MEDIA_PREFIX = "media:"

    @staticmethod
    def retrieve_page(lookup_field_value) -> Page | None:
        try:
            return Page.objects.get(pk=lookup_field_value)
        except (Page.DoesNotExist, Page.MultipleObjectsReturned):
            return None

    @staticmethod
    def retrieve_document(lookup_field_value: str) -> "Model | None":
        try:
            return get_document_model().objects.get(pk=lookup_field_value)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None

    @staticmethod
    def retrieve_image(lookup_field_value: str) -> "Model | None":
        try:
            return get_image_model().objects.get(pk=lookup_field_value)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None

    @staticmethod
    def retrieve_wagtailmedia(lookup_field_value: str) -> "Model | None":
        if not apps.is_installed("wagtailmedia"):
            return None

        try:
            from wagtailmedia.models import get_media_model

            return get_media_model().objects.get(pk=lookup_field_value)
        except (ObjectDoesNotExist, MultipleObjectsReturned):
            return None

    @classmethod
    def retrieve(cls, url: str) -> "Model | None":
        pairs = (
            (cls.PAGE_LINK_PREFIX, cls.retrieve_page),
            (cls.DOCUMENT_LINK_PREFIX, cls.retrieve_document),
            (cls.IMAGE_PREFIX, cls.retrieve_image),
            (cls.MEDIA_PREFIX, cls.retrieve_wagtailmedia),
        )
        for prefix, object_retrieve_method in pairs:
            if url.startswith(prefix):
                return object_retrieve_method(url.replace(prefix, ""))

        return None


# python-markdown stores backslash-escaped characters as STX<code point>ETX
# until its last processing step.
ESCAPED_CHAR_RE = re.compile(f"{util.STX}(\\d+){util.ETX}")


def _unescape(text: str) -> str:
    return ESCAPED_CHAR_RE.sub(lambda m: chr(int(m.group(1))), text)


@dataclass
class TemplateImage:
    """An image to render with the `image_template` setting's template."""

    image: "Model"
    alt: str
    css_class: str
    caption: str
    filter_spec: str | None


class ImageProcessor(ImageInlineProcessor):
    def __init__(self, object_lookup_negotiator, *args, template_name=None, **kwargs):
        self.object_lookup_negotiator = object_lookup_negotiator
        self.template_name = template_name
        super().__init__(*args, **kwargs)

    def handleMatch(self, m, data):
        element, processed_m, index = super().handleMatch(m, data)
        if element is None:
            return element, processed_m, index

        pk, *opts_str = element.get("src", "").split(",", 1)
        image = self.object_lookup_negotiator.retrieve(pk)
        if image and self.template_name:
            opts = _options_to_dict(opts_str[0]) if opts_str else {}
            return self._placeholder(image, element, opts), processed_m, index
        if image:
            opts = _options_to_dict(opts_str[0]) if opts_str else {}
            element.set("class", opts.get("class", "left"))

            rendition = self._get_rendition(image, opts.get("filter", "width-500"))
            element.set("src", rendition.url)
            element.set("width", str(rendition.width))
            element.set("height", str(rendition.height))
        return element, processed_m, index

    def _placeholder(self, image, element, opts) -> etree.Element:
        """
        Keep the image aside and return a placeholder token for it, which
        `render_markdown` replaces with the rendered template after sanitising.
        The token is letters and digits only, so Markdown leaves it alone. Until
        `render_markdown` unwraps it, it is the tag name of an empty element, so
        it isn't part of the text around it, such as the heading text `toc` uses
        for ids.
        """
        images = self.md.wagtailmarkdown_images
        images.items.append(
            TemplateImage(
                image=image,
                # Kept outside the element tree, so escapes such as \[ are
                # restored here rather than by Markdown itself.
                alt=_unescape(element.get("alt", "")),
                css_class=opts.get("class", "left"),
                caption=_unescape(element.get("title", "")),
                filter_spec=opts.get("filter"),
            )
        )
        return etree.Element(f"{images.token}{len(images.items) - 1}")

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


@dataclass
class ImagePlaceholders:
    """The images held back for a template in one Markdown instance."""

    template_name: str
    token: str = field(
        default_factory=lambda: f"WAGTAILMARKDOWNIMAGE{secrets.token_hex(8)}N"
    )
    items: list[TemplateImage] = field(default_factory=list)


class ImageExtension(Extension):
    def __init__(
        self,
        object_lookup_negotiator: ObjectLookupNegotiator | None = None,
        template_name: str | None = None,
        **kwargs,
    ):
        self.object_lookup_negotiator = (
            object_lookup_negotiator or ObjectLookupNegotiator
        )
        self.template_name = template_name
        super().__init__(**kwargs)

    def extendMarkdown(self, md: "Markdown") -> None:
        md.inlinePatterns.register(
            ImageProcessor(
                pattern=IMAGE_LINK_RE,
                md=md,
                object_lookup_negotiator=self.object_lookup_negotiator,
                template_name=self.template_name,
            ),
            "image_link",
            151,
        )
        if self.template_name:
            md.wagtailmarkdown_images = ImagePlaceholders(
                template_name=self.template_name
            )


class LinkExtension(Extension):
    def __init__(
        self,
        object_lookup_negotiator: ObjectLookupNegotiator | None = None,
        **kwargs,
    ):
        self.object_lookup_negotiator = (
            object_lookup_negotiator or ObjectLookupNegotiator
        )
        super().__init__(**kwargs)

    def extendMarkdown(self, md: "Markdown") -> None:
        md.inlinePatterns.register(
            LinkProcessor(
                pattern=LINK_RE,
                md=md,
                object_lookup_negotiator=self.object_lookup_negotiator,
            ),
            "link",
            161,
        )


class DelExtension(Extension):
    def extendMarkdown(self, md: "Markdown") -> None:
        """Supports ~TEXT~ and ~~TEXT~~ syntax."""
        md.inlinePatterns.register(
            SimpleTagInlineProcessor(r"(\~{1,2})(.+?)\1", "del"), "tilde del", 170
        )
