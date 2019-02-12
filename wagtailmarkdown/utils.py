# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# felicity@torchbox.com 2015-09-14
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#
import importlib
import warnings

from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe

import bleach
import markdown

from .mdx import linker, tables
from .warnings import WagtailMarkdownDeprecationWarning


def render_markdown(text, context=None, extensions=''):
    """
    Turn markdown into HTML.
    """
    if context is None or not isinstance(context, dict):
        context = {}
    markdown_html = _transform_markdown_into_html(text, extensions)
    sanitised_markdown_html = _sanitise_markdown_html(markdown_html, extensions)
    return mark_safe(sanitised_markdown_html)


def _transform_markdown_into_html(text, extensions):
    markdown_kwargs = _get_markdown_kwargs()
    markdown_kwargs['extensions'] += extensions.split()
    return markdown.markdown(smart_text(text), **markdown_kwargs)


def _sanitise_markdown_html(markdown_html, extensions):
    """Ask the extensions in the string extensions what extra markup they allow
       and combine with default keyword arguments to bleach.clean.

       Note that we only process the 'tags', 'attributes', and 'styles' keywords.
    """
    bleach_kwargs = _get_base_bleach_kwargs()
    for extension_name in extensions.split():
        extra = _get_extension_bleach_kwargs(extension_name)
        if "tags" in extra:
            for tag in extra["tags"]:
                if tag not in bleach_kwargs["tags"]:
                    bleach_kwargs["tags"].append(tag)
        if "attributes" in extra:
            for tag, attrs in extra["attributes"].items():
                for att in attrs:
                    if att not in bleach_kwargs["attributes"][tag]:
                        bleach_kwargs["attributes"][tag].append(att)
        if "styles" in extra:
            for style in extra["styles"]:
                if style not in bleach_kwargs["styles"]:
                    bleach_kwargs["styles"].append(style)

    return bleach.clean(markdown_html, **bleach_kwargs)


def _get_extension_bleach_kwargs(extension_name):
    """Use the lookup algorithm for python-markdown to find an extension class or module.

       If the extension specifier gives a class (is 'module:classname') we look
       for class variable 'allowed_markup'.
       If the extension specifier if a module we look for a module level
       variable 'allowed_markup'.
       In each case the result is a dictionary of keyword args that will be
       recursively merged with the defaults (see the calling function,
       _sanitize_markdown_html).

       If allowed_markup is not found return {}.

       We do not currently recognize either deprrecated or version 2+ only
       syntax for specifying extensions.
    """
    # Get class name (if provided): `path.to.module:ClassName`
    ext_name, class_name = extension_name.split(':', 1) \
        if ':' in extension_name else (extension_name, '')

    try:
        module = importlib.import_module(ext_name)
    except ImportError:
        return {}
    try:
      if class_name:
            return getattr(module, class_name).allowed_markup
      else:
            return module.allowed_markup
    except AttributeError:
        return {}

def _get_base_bleach_kwargs():
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


def _get_markdown_kwargs():
    markdown_kwargs = {}
    markdown_kwargs['extensions'] = [
        'extra',
        'codehilite',
        tables.TableExtension(),
        linker.LinkerExtension({
             '__default__': 'wagtailmarkdown.mdx.linkers.page',
             'page:': 'wagtailmarkdown.mdx.linkers.page',
             'image:': 'wagtailmarkdown.mdx.linkers.image',
             'doc:': 'wagtailmarkdown.mdx.linkers.document',
         })
    ]
    markdown_kwargs['extension_configs'] = {
        'codehilite': [
            ('guess_lang', False),
        ]
    }
    markdown_kwargs['output_format'] = 'html5'
    return markdown_kwargs


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
