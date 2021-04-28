# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# felicity@torchbox.com 2015-09-14
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#
from django.conf import settings
from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe

import bleach
import markdown

from .mdx import linker, tables


def render_markdown(text, context=None):
    """
    Turn markdown into HTML.
    """
    if context is None or not isinstance(context, dict):
        context = {}
    markdown_html = _transform_markdown_into_html(text)
    sanitised_markdown_html = _sanitise_markdown_html(markdown_html)
    return mark_safe(sanitised_markdown_html)


def _transform_markdown_into_html(text):
    return markdown.markdown(smart_text(text), **_get_markdown_kwargs())


def _sanitise_markdown_html(markdown_html):
    return bleach.clean(markdown_html, **_get_bleach_kwargs())


def _get_bleach_kwargs():
    bleach_kwargs = {}
    bleach_kwargs["tags"] = [
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
    ]
    bleach_kwargs["attributes"] = {
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
    }
    bleach_kwargs["styles"] = [
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
    ]
    return bleach_kwargs


def _get_markdown_kwargs():
    markdown_kwargs = {}
    markdown_kwargs["extensions"] = [
        "extra",
        "codehilite",
        tables.TableExtension(),
        linker.LinkerExtension(
            {
                "__default__": "wagtailmarkdown.mdx.linkers.page",
                "page:": "wagtailmarkdown.mdx.linkers.page",
                "image:": "wagtailmarkdown.mdx.linkers.image",
                "doc:": "wagtailmarkdown.mdx.linkers.document",
            }
        ),
    ]

    if hasattr(settings, "WAGTAILMARKDOWN_EXTENSIONS"):
        markdown_kwargs["extensions"] += settings.WAGTAILMARKDOWN_EXTENSIONS

    markdown_kwargs["extension_configs"] = {
        "codehilite": [
            ("guess_lang", False),
        ]
    }

    if hasattr(settings, "WAGTAILMARKDOWN_EXTENSIONS_CONFIG"):
        markdown_kwargs["extension_configs"].update(
            settings.WAGTAILMARKDOWN_EXTENSIONS_CONFIG
        )

    markdown_kwargs["output_format"] = "html5"
    return markdown_kwargs
