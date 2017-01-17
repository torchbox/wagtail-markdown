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
from django.db.models import TextField
from django.utils.translation import ugettext_lazy as _

from wagtail.utils.widgets import WidgetWithScript
from wagtail.wagtailcore.blocks import TextBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel

import wagtailmarkdown.utils


class MarkdownTextarea(WidgetWithScript, forms.widgets.Textarea):
    def __init__(self, **kwargs):
        super(MarkdownTextarea, self).__init__(**kwargs)

    def render_js_init(self, id_, name, value):
        return 'simplemdeAttach("{0}");'.format(id_)

    @property
    def media(self):
        return forms.Media(
            css = { 'all': ( 'wagtailmarkdown/css/simplemde.min.css', ) },
            js = (
                'wagtailmarkdown/js/simplemde.min.js',
                'wagtailmarkdown/js/simplemde.attach.js',
            )
        )


class MarkdownBlock(TextBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        self.field = forms.CharField(required=required, help_text=help_text, widget=MarkdownTextarea())
        super(MarkdownBlock, self).__init__(**kwargs)

    def render_basic(self, value, context=None):
        return wagtailmarkdown.utils.render(value)

    @property
    def media(self):
        return forms.Media(
            css = { 'all': ( 'wagtailmarkdown/css/simplemde.min.css', ) },
            js = (
                'wagtailmarkdown/js/simplemde.min.js',
                'wagtailmarkdown/js/simplemde.attach.js',
            )
        )


class MarkdownField(TextField):
    def formfield(self, **kwargs):
        defaults = {'widget': MarkdownTextarea}                                                  
        defaults.update(kwargs)                                                              
        return super(MarkdownField, self).formfield(**defaults)                              

    def __init__(self, **kwargs):
        super(MarkdownField, self).__init__(**kwargs)


class MarkdownPanel(FieldPanel):
    def __init__(self, field_name, classname="", widget=None):
        super(MarkdownPanel, self).__init__(field_name, classname, widget)
