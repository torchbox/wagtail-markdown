# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# felicity@torchbox.com 2015-09-14
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#

from wagtail.wagtailcore import hooks
from django.utils.html import format_html, format_html_join
from django.conf import settings

@hooks.register('insert_editor_js')
def load_simplemde_js():
    js_files = [
        'wagtailmarkdown/js/simplemde.min.js',
    ]
    js_includes = format_html_join('\n', '<script src="{0}{1}"></script>',
        ((settings.STATIC_URL, filename) for filename in js_files)
    )
    return js_includes + """
<script>
$(document).ready(function() {
    $(".markdown textarea").each(function(index, elem) {
        var mde = new SimpleMDE({
            element: elem,
            spellChecker: false,
            toolbar: false,
            autofocus: false,
        });
        mde.render();
    });
});
</script>
"""

@hooks.register('insert_editor_css')
def load_simplemde_css():
    return format_html('<link rel="stylesheet" href="' + settings.STATIC_URL + 'wagtailmarkdown/css/simplemde.min.css">')
