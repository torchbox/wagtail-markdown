# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# felicity@torchbox.com 2015-09-14
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#
import warnings

from django.utils.safestring import mark_safe

import bleach
import markdown
from markdown.extensions.tables import TableExtension
from wagtailmarkdown import inlinepatterns
from wagtailmarkdown.warnings import WagtailMarkdownDeprecationWarning

try:
    from wagtail.wagtailimages import get_image_model
    from wagtail.wagtailcore.models import Page
    from wagtail.wagtaildocs.models import Document
except ImportError:
    from wagtail.images import get_image_model
    from wagtail.core.models import Page
    from wagtail.documents.models import Document


class LinkExtension(markdown.Extension):
    def __init__(self, object_lookup_negotiator, *args, **kwargs):
        self.object_lookup_negotiator = object_lookup_negotiator

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['link'] = inlinepatterns.LinkPattern(
            pattern=markdown.inlinepatterns.LINK_RE,
            markdown_instance=md,
            object_lookup_negotiator=self.object_lookup_negotiator,
        )


class ImageExtension(markdown.Extension):
    def __init__(self, object_lookup_negotiator, *args, **kwargs):
        self.object_lookup_negotiator = object_lookup_negotiator

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns['image_link'] = inlinepatterns.ImagePattern(
            pattern=markdown.inlinepatterns.IMAGE_LINK_RE,
            markdown_instance=md,
            object_lookup_negotiator=self.object_lookup_negotiator,
        )


class ObjectLookupNegotiator:
    PAGE_LINK_PREFIX = 'page:'
    DOCUMENT_LINK_PREFIX = 'doc:'
    IMAGE_PREFIX = 'image:'

    @staticmethod
    def retrieve_page(lookup_field_value):
        return Page.objects.get(pk=lookup_field_value)

    @staticmethod
    def retrieve_document(lookup_field_value):
        return Document.objects.get(pk=lookup_field_value)

    @staticmethod
    def retrieve_image(lookup_field_value):
        return get_image_model().objects.get(pk=lookup_field_value)

    @classmethod
    def retrieve(cls, url):
        pairs = (
            (cls.PAGE_LINK_PREFIX, cls.retrieve_page),
            (cls.DOCUMENT_LINK_PREFIX, cls.retrieve_document),
            (cls.IMAGE_PREFIX, cls.retrieve_image)
        )
        for prefix, object_retrieve_method in pairs:
            if url.startswith(prefix):
                return object_retrieve_method(url.replace(prefix, ''))


def render_markdown(text, object_lookup_negotiator=ObjectLookupNegotiator):
    html = markdown.markdown(
        text,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            TableExtension(),
            LinkExtension(object_lookup_negotiator=object_lookup_negotiator),
            ImageExtension(object_lookup_negotiator=object_lookup_negotiator),
        ],
        extension_configs={
            'codehilite': [
                ('guess_lang', False),
            ]
        },
        output_format='html5'
    )
    sanitised_html = _sanitise_markdown_html(html)
    return mark_safe(sanitised_html)


def _sanitise_markdown_html(markdown_html):
    return bleach.clean(markdown_html, **_get_bleach_kwargs())


def _get_bleach_kwargs():
    bleach_kwargs = {}
    bleach_kwargs['tags'] = [
        'p',
        'div',
        'span',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'tt',
        'pre',
        'em',
        'strong',
        'ul',
        'li',
        'dl',
        'dd',
        'dt',
        'code',
        'img',
        'a',
        'table',
        'tr',
        'th',
        'td',
        'tbody',
        'caption',
        'colgroup',
        'thead',
        'tfoot',
        'blockquote',
        'ol',
        'hr',
        'br',
    ]
    bleach_kwargs['attributes'] = {
        '*': [
            'class',
            'style',
            'id',
        ],
        'a': [
            'href',
            'target',
            'rel',
        ],
        'img': [
            'src',
            'alt',
        ],
        'tr': [
            'rowspan',
            'colspan',
        ],
        'td': [
            'rowspan',
            'colspan',
            'align',
        ],
    }
    bleach_kwargs['styles'] = [
        'color',
        'background-color',
        'font-family',
        'font-weight',
        'font-size',
        'width',
        'height',
        'text-align',
        'border',
        'border-top',
        'border-bottom',
        'border-left',
        'border-right',
        'padding',
        'padding-top',
        'padding-bottom',
        'padding-left',
        'padding-right',
        'margin',
        'margin-top',
        'margin-bottom',
        'margin-left',
        'margin-right',
    ]
    return bleach_kwargs


def render(text, context=None):
    """
    Depreceated call to render_markdown().
    """
    warning = (
        "wagtailmarkdown.utils.render() is deprecated. Use "
        "wagtailmarkdown.utils.render_markdown() instead."
    )
    warnings.warn(warning, WagtailMarkdownDeprecationWarning, stacklevel=2)
    return render_markdown(text, context)
