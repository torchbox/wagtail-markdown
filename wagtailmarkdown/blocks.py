# vim:sw=4 ts=4 et:
# Copyright (c) 2015 Torchbox Ltd.
# tomasz.knapik@torchbox.com 2017-12-07
#
# Permission is granted to anyone to use this software for any purpose,
# including commercial applications, and to alter it and redistribute it
# freely. This software is provided 'as-is', without any express or implied
# warranty.
#
from django import forms

from .utils import render_markdown
from .widgets import MarkdownTextarea

try:
    from wagtail.core.blocks import TextBlock
except ImportError:
    from wagtail.wagtailcore.blocks import TextBlock


class MarkdownBlock(TextBlock):
    def __init__(self, required=True, help_text=None, **kwargs):
        self.field = forms.CharField(
            required=required, help_text=help_text, widget=MarkdownTextarea()
        )
        super(MarkdownBlock, self).__init__(**kwargs)

    def render_basic(self, value, context=None):
        return render_markdown(value, context)
