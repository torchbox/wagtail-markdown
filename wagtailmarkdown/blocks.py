# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# felicity@torchbox.com 2015-09-14
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#


from django import forms
from wagtail.utils.widgets import WidgetWithScript
from wagtail.wagtailcore.blocks import TextBlock
import wagtailmarkdown.utils


class MarkdownTextarea(WidgetWithScript, forms.widgets.Textarea):
    def __init__(self, **kwargs):
        super(MarkdownTextarea, self).__init__(**kwargs)

    def render_js_init(self, id_, name, value):
        return 'simplemdeAttach("{0}");'.format(id_)


class MarkdownBlock(TextBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        if 'classname' in kwargs:
            kwargs['classname'] += ' markdown'
        else:
            kwargs['classname'] = 'markdown'
        self.field = forms.CharField(required=required, help_text=help_text, widget=MarkdownTextarea())
        super(MarkdownBlock, self).__init__(**kwargs)

    def render_basic(self, value):
        return wagtailmarkdown.utils.render(value)

    class Media:
        css = { 'all': ( 'wagtailmarkdown/css/simplemde.min.css', ) }
        js = (
            'wagtailmarkdown/js/simplemde.min.js',
            'wagtailmarkdown/js/simplemde.attach.js',
        )
