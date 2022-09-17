from django.conf import settings
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe

import bleach
import markdown

from .mdx import linker


def render_markdown(text, context=None):
    """
    Turn markdown into HTML.
    """
    markdown_html = _transform_markdown_into_html(text)
    sanitised_markdown_html = _sanitise_markdown_html(markdown_html)
    return mark_safe(sanitised_markdown_html)


def _transform_markdown_into_html(text):
    return markdown.markdown(smart_str(text), **_get_markdown_kwargs())


def _sanitise_markdown_html(markdown_html):
    return bleach.clean(markdown_html, **_get_bleach_kwargs())


def _get_default_bleach_kwargs():
    return {
        "tags": [
            "p",
            "div",
            "span",
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "tt",
            "pre",
            "em",
            "strong",
            "ul",
            "sup",
            "li",
            "dl",
            "dd",
            "dt",
            "code",
            "img",
            "a",
            "table",
            "tr",
            "th",
            "td",
            "tbody",
            "caption",
            "colgroup",
            "thead",
            "tfoot",
            "blockquote",
            "ol",
            "hr",
            "br",
        ],
        "attributes": {
            "*": [
                "class",
                "style",
                "id",
            ],
            "a": [
                "href",
                "target",
                "rel",
            ],
            "img": [
                "src",
                "alt",
            ],
            "tr": [
                "rowspan",
                "colspan",
            ],
            "td": [
                "rowspan",
                "colspan",
                "align",
            ],
        },
        "styles": [
            "color",
            "background-color",
            "font-family",
            "font-weight",
            "font-size",
            "width",
            "height",
            "text-align",
            "border",
            "border-top",
            "border-bottom",
            "border-left",
            "border-right",
            "padding",
            "padding-top",
            "padding-bottom",
            "padding-left",
            "padding-right",
            "margin",
            "margin-top",
            "margin-bottom",
            "margin-left",
            "margin-right",
        ],
    }


def _get_bleach_kwargs():
    bleach_kwargs = _get_default_bleach_kwargs()

    if hasattr(settings, "WAGTAILMARKDOWN"):
        if "allowed_styles" in settings.WAGTAILMARKDOWN:
            bleach_kwargs["styles"] = list(
                set(
                    settings.WAGTAILMARKDOWN["allowed_styles"] + bleach_kwargs["styles"]
                )
            )
        if "allowed_tags" in settings.WAGTAILMARKDOWN:
            bleach_kwargs["tags"] = list(
                set(settings.WAGTAILMARKDOWN["allowed_tags"] + bleach_kwargs["tags"])
            )
        if "allowed_attributes" in settings.WAGTAILMARKDOWN:
            bleach_kwargs["attributes"] = {
                **bleach_kwargs["attributes"],
                **settings.WAGTAILMARKDOWN["allowed_attributes"],
            }

    return bleach_kwargs


def _get_default_markdown_kwargs():
    markdown_kwargs = {
        "extensions": [
            "extra",
            "codehilite",
            "tables",
            linker.LinkerExtension(
                {
                    "__default__": "wagtailmarkdown.mdx.linkers.page",
                    "page:": "wagtailmarkdown.mdx.linkers.page",
                    "image:": "wagtailmarkdown.mdx.linkers.image",
                    "doc:": "wagtailmarkdown.mdx.linkers.document",
                }
            ),
        ],
        "extension_configs": {
            "codehilite": [
                ("guess_lang", False),
            ]
        },
        "output_format": "html5",
    }

    return markdown_kwargs


def _get_markdown_kwargs():
    markdown_kwargs = _get_default_markdown_kwargs()

    if (
        hasattr(settings, "WAGTAILMARKDOWN")
        and "extensions" in settings.WAGTAILMARKDOWN
    ):
        markdown_kwargs["extensions"] = list(
            set(markdown_kwargs["extensions"] + settings.WAGTAILMARKDOWN["extensions"])
        )

    if (
        hasattr(settings, "WAGTAILMARKDOWN")
        and "extension_configs" in settings.WAGTAILMARKDOWN
    ):
        markdown_kwargs["extension_configs"].update(
            settings.WAGTAILMARKDOWN["extension_configs"]
        )

    return markdown_kwargs
