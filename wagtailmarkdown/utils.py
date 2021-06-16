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
import warnings

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
    
    if hasattr(settings, "WAGTAILMARKDOWN"):
        if 'allowed_styles' in settings.WAGTAILMARKDOWN:
            bleach_kwargs["styles"]=bleach_kwargs["styles"]+list(set(settings.WAGTAILMARKDOWN['allowed_styles']) - set(bleach_kwargs["styles"]))
        if 'allowed_tags' in settings.WAGTAILMARKDOWN:
            bleach_kwargs["tags"]=bleach_kwargs["tags"]+list(set(settings.WAGTAILMARKDOWN['allowed_tags']) - set(bleach_kwargs["tags"]))
        if 'allowed_attributes' in settings.WAGTAILMARKDOWN:
            bleach_kwargs["attributes"]={**bleach_kwargs["attributes"],**settings.WAGTAILMARKDOWN['allowed_attributes']}            
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
        warnings.warn(
            "WAGTAILMARKDOWN_EXTENSIONS will be deprecated in version 7.1, use WAGTAILMARKDOWN = { extensions: {} } as dict instead",
             PendingDeprecationWarning
        )
    elif hasattr(settings, "WAGTAILMARKDOWN") and 'extensions' in settings.WAGTAILMARKDOWN:
        markdown_kwargs["extensions"] += settings.WAGTAILMARKDOWN['extensions']

    markdown_kwargs["extension_configs"] = {
        "codehilite": [
            ("guess_lang", False),
        ]
    }

    if hasattr(settings, "WAGTAILMARKDOWN_EXTENSIONS_CONFIG"):
        markdown_kwargs["extension_configs"].update(
            settings.WAGTAILMARKDOWN_EXTENSIONS_CONFIG
        )
        warnings.warn(
            "WAGTAILMARKDOWN_EXTENSIONS_CONFIG will be deprecated in version 7.1, use WAGTAILMARKDOWN = { extensions_config: {} } as dict instead",
             PendingDeprecationWarning
        )
    elif hasattr(settings, "WAGTAILMARKDOWN") and 'extensions_config' in settings.WAGTAILMARKDOWN:
        markdown_kwargs["extension_configs"].update(
            settings.WAGTAILMARKDOWN['extensions_config']
        )

    markdown_kwargs["output_format"] = "html5"
    return markdown_kwargs
