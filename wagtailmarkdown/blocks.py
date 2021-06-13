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
from django.utils.functional import cached_property

from .utils import render_markdown
from .widgets import MarkdownTextarea

try:
    from wagtail.core.blocks import TextBlock
except ImportError:
    from wagtail.wagtailcore.blocks import TextBlock


class MarkdownBlock(TextBlock):
    @cached_property
    def field(self):
        field_kwargs = {"widget": MarkdownTextarea(attrs={"rows": self.rows})}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def render_basic(self, value, context=None):
        return render_markdown(value, context)
