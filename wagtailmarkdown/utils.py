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

from django.utils.encoding import smart_text
from django.utils.safestring import mark_safe

import bleach
import markdown

# comes with wagtail
from bs4 import BeautifulSoup

from .mdx import linker, tables
from .warnings import WagtailMarkdownDeprecationWarning


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


# class TexFilter(bleach.html5lib_shim.Filter):
#     def __iter__(self):
#         open_scripts=[]
#         for token in bleach.html5lib_shim.Filter.__iter__(self):
#             print(token)
#             type_ = token['type']
#             if type_ in ['StartTag','EndTag'] and token['name'] in ['script'] and token['data']:

#                 for k,v in token['data'].items():
#                     print(k,v)
                
#                 if (None, 'type') in token['data']:
#                     print("hit1")
#                     if token['data'][(None, 'type')] in ["math/tex; mode=display", "math/tex", "js"]:
#                         print("hit2")
#                         yield token
#                 else:
#                     print('miss')
#             else:
#                 yield token


def _sanitise_markdown_html(markdown_html):
    # Would be more beautiful with a filter but I have no clue how to deal with the flatness of the iterator
    # https://html5lib.readthedocs.io/en/latest/_modules/html5lib/filters/lint.html#Filter
    # One needs a memory (open_elements)
    # The solution below is much cleaner

    # cleaner = bleach.sanitizer.Cleaner(**_get_bleach_kwargs(), filters=[TexFilter])
    # return cleaner.clean(markdown_html)

    cleaned_html = bleach.clean(markdown_html, **_get_bleach_kwargs())

    # Problem: <script> tags get removed
    # See: https://github.com/mozilla/bleach/issues/330 .. 
    # this routine here is needed because bleach doesn't
    # have conditional tag whitelists.
    soup = BeautifulSoup(cleaned_html, 'html5lib')
    for script_tag in soup.find_all('script'):
        if script_tag.attrs.get('type', False) not in ['math/tex; mode=display','math/tex' ]:
            # remove this script. it isn't MathJax.
            script_tag.extract()
    
    return str(soup)


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
        'sup',
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
        # white list <script>
        'script'
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
        'script': [
            'type',
        ]
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
        }),
        'mdx_math'
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
