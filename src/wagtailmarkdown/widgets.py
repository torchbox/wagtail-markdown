from django import forms
from django.conf import settings

from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.telepath import register
from wagtail.utils.widgets import WidgetWithScript
from wagtail.widget_adapters import WidgetAdapter


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
        css = (
            "wagtailmarkdown/css/easymde.min.css",
            "wagtailmarkdown/css/easymde.tweaks.css",
        )
        if WAGTAIL_VERSION >= (5, 0):
            css += ("wagtailmarkdown/css/easymde.darkmode.css",)

        return forms.Media(
            css={"all": css},
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
