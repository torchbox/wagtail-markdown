from django import forms
from django.utils.functional import cached_property
from wagtail.blocks import TextBlock

from .utils import render_markdown
from .widgets import MarkdownTextarea


class MarkdownBlock(TextBlock):
    @cached_property
    def field(self):
        field_kwargs = {"widget": MarkdownTextarea(attrs={"rows": self.rows})}
        field_kwargs.update(self.field_options)
        return forms.CharField(**field_kwargs)

    def render_basic(self, value, context=None):
        return render_markdown(value, context)
