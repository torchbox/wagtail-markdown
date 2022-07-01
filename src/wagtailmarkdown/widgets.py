from django import forms
from django.conf import settings

from wagtail.core.telepath import register
from wagtail.core.widget_adapters import WidgetAdapter
from wagtail.utils.widgets import WidgetWithScript


class MarkdownTextarea(WidgetWithScript, forms.widgets.Textarea):
    def render_js_init(self, id_, name, value):
        if (
            hasattr(settings, "WAGTAILMARKDOWN")
            and "autodownload_fontawesome" in settings.WAGTAILMARKDOWN
        ):
            autodownload = (
                "true"
                if settings.WAGTAILMARKDOWN["autodownload_fontawesome"]
                else "false"
            )
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
