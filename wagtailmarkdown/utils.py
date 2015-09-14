# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# felicity@torchbox.com 2015-09-14
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#

from django.utils.safestring import mark_safe
import markdown

import wagtailmarkdown.mdx.tables
import wagtailmarkdown.mdx.linker

def render(text):
    return mark_safe(markdown.markdown(text,
        extensions=[ 'extra',
                     'codehilite',
                     wagtailmarkdown.mdx.tables.TableExtension(),
                     wagtailmarkdown.mdx.linker.LinkerExtension({
                         '__default__':  'wagtailmarkdown.mdx.linkers.page',
                         'page:':        'wagtailmarkdown.mdx.linkers.page',
                         'image:':       'wagtailmarkdown.mdx.linkers.image',
                         'doc:':         'wagtailmarkdown.mdx.linkers.document',
                     })
                   ],
        extension_configs = {
            'codehilite': [
                ('guess_lang', False),
            ]
        },
        output_format='html5',
        safe_mode='escape'))
