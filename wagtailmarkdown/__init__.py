# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# felicity@torchbox.com 2015-09-14
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#

from django.db.models import TextField
from django.utils.translation import ugettext_lazy as _

from wagtail.wagtailcore.blocks import TextBlock
from wagtail.wagtailadmin.edit_handlers import FieldPanel

import wagtailmarkdown.utils

class MarkdownBlock(TextBlock):
    def render_basic(self, value):
        return wagtailmarkdown.utils.render(value)

class MarkdownField(TextField):
    def __init__(self, **kwargs):
        if 'help_text' not in kwargs:
            kwargs['help_text'] = 'Use <em>*emphasised*</em> or **strong** text, link to <:Another page> or include <:image:An image.jpeg>.'
        super(MarkdownField, self).__init__(**kwargs)

class MarkdownPanel(FieldPanel):
    def __init__(self, field_name, classname="", widget=None):
        super(MarkdownPanel, self).__init__(field_name, classname, None)

        if self.classname != "":
            self.classname += " "
        self.classname += "markdown"
