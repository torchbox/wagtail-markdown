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
from django.conf import settings

from wagtail.utils.widgets import WidgetWithScript

import warnings

try:
    from wagtail.core.telepath import register
    from wagtail.core.widget_adapters import WidgetAdapter
except ImportError:  # do-nothing fallback for Wagtail <2.13

    def register(adapter, cls):
        pass

    class WidgetAdapter:
        pass


class MarkdownTextarea(WidgetWithScript, forms.widgets.Textarea):
    def render_js_init(self, id_, name, value):
        autodownload_fontawesome = None
        if hasattr(settings, "WAGTAILMARKDOWN") and 'autodownload_fontawesome' in settings.WAGTAILMARKDOWN:
            autodownload_fontawesome = "true" if a settings.WAGTAILMARKDOWN["autodownload_fontawesome"] else "false"
        if autodownload_fontawesome is None:
            autodownload_fontawesome = getattr(
                settings, "WAGTAILMARKDOWN_AUTODOWNLOAD_FONTAWESOME", None
            )
            if hasattr(settings, "WAGTAILMARKDOWN_AUTODOWNLOAD_FONTAWESOME"):
                warnings.warn(
                "WAGTAILMARKDOWN_AUTODOWNLOAD_FONTAWESOME will be deprecated in version 7.1, use WAGTAILMARKDOWN = { autodownload_fontawesome: .. } as dict instead",
                 PendingDeprecationWarning
                )
        if autodownload_fontawesome is not None:
            autodownload = "true" if autodownload_fontawesome else "false"
            return 'easymdeAttach("{0}", {1});'.format(id_, autodownload)
        return 'easymdeAttach("{0}");'.format(id_)

    @property
    def media(self):
        return forms.Media(
            css={
                "all": (
                    "wagtailmarkdown/css/easymde.min.css",
                    "wagtailmarkdown/css/easymde.tweaks.css",
                )
            },
            js=(
                "wagtailmarkdown/js/easymde.min.js",
                "wagtailmarkdown/js/easymde.attach.js",
            ),
        )


class MarkdownTextareaAdapter(WidgetAdapter):
    js_constructor = "wagtailmarkdown.widgets.MarkdownTextarea"

    class Media:
        js = ["wagtailmarkdown/js/markdown-textarea-adapter.js"]


register(MarkdownTextareaAdapter(), MarkdownTextarea)
