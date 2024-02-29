from django import forms
from django.conf import settings
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.telepath import register
from wagtail.widget_adapters import WidgetAdapter


if WAGTAIL_VERSION >= (6, 0):

    class MarkdownTextarea(forms.widgets.Textarea):  # type: ignore PGH003
        def build_attrs(self, *args, **kwargs):
            attrs = super().build_attrs(*args, **kwargs)
            attrs["data-controller"] = "easymde"

            if (
                hasattr(settings, "WAGTAILMARKDOWN")
                and "autodownload_fontawesome" in settings.WAGTAILMARKDOWN
            ):
                autodownload = (
                    "true"
                    if settings.WAGTAILMARKDOWN["autodownload_fontawesome"]
                    else "false"
                )
                attrs["data-easymde-autodownload-value"] = autodownload

            return attrs

        @property
        def media(self):
            css = (
                "wagtailmarkdown/css/easymde.min.css",
                "wagtailmarkdown/css/easymde.tweaks.css",
            )

            return forms.Media(
                css={"all": css},
                js=(
                    "wagtailmarkdown/js/easymde.min.js",
                    "wagtailmarkdown/js/easymde.attach.js",
                    "wagtailmarkdown/js/easymde-controller.js",
                ),
            )

else:
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
                return f'easymdeAttach("{id_}", {autodownload});'

            return f'easymdeAttach("{id_}");'

        @property
        def media(self):
            css = (
                "wagtailmarkdown/css/easymde.min.css",
                "wagtailmarkdown/css/easymde.tweaks.css",
            )

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
