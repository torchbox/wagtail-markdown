from django import template

from ..utils import render_markdown


register = template.Library()


@register.filter(name="markdown")
def markdown(value):
    return render_markdown(value)
