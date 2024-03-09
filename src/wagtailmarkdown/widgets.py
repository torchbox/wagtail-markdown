from django import forms
from django.conf import settings
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.staticfiles import versioned_static


class MarkdownTextareaBase(forms.Textarea):
    def _get_media_js(self):
        return (
            versioned_static("wagtailmarkdown/js/easymde.min.js"),
            versioned_static("wagtailmarkdown/js/easymde.attach.js"),
        )

    @property
    def media(self):
        css = (
            versioned_static("wagtailmarkdown/css/easymde.min.css"),
            versioned_static("wagtailmarkdown/css/easymde.tweaks.css"),
        )

        return forms.Media(css={"all": css}, js=self._get_media_js())


if WAGTAIL_VERSION >= (6, 0):

    class MarkdownTextarea(MarkdownTextareaBase):
        def build_attrs(self, *args, **kwargs):
            attrs = super().build_attrs(*args, **kwargs)
            attrs["data-controller"] = "easymde"

            if "autodownload_fontawesome" in getattr(settings, "WAGTAILMARKDOWN", {}):
                autodownload = (
                    "true"
                    if settings.WAGTAILMARKDOWN["autodownload_fontawesome"]
                    else "false"
                )
                attrs["data-easymde-autodownload-value"] = autodownload

            return attrs

        def _get_media_js(self):
            return (
                versioned_static("wagtailmarkdown/js/easymde.min.js"),
                versioned_static("wagtailmarkdown/js/easymde.attach.js"),
                versioned_static("wagtailmarkdown/js/easymde-controller.js"),
            )

else:
    from wagtail.telepath import register
    from wagtail.utils.widgets import WidgetWithScript
    from wagtail.widget_adapters import WidgetAdapter

    class MarkdownTextarea(WidgetWithScript, MarkdownTextareaBase):
        def render_js_init(self, id_, name, value):
            if "autodownload_fontawesome" in getattr(settings, "WAGTAILMARKDOWN", {}):
                autodownload = (
                    "true"
                    if settings.WAGTAILMARKDOWN["autodownload_fontawesome"]
                    else "false"
                )
                return f'easymdeAttach("{id_}", {autodownload});'

            return f'easymdeAttach("{id_}");'

    class MarkdownTextareaAdapter(WidgetAdapter):
        js_constructor = "wagtailmarkdown.widgets.MarkdownTextarea"

        class Media:
            # TODO: remove the adapter when dropping support for Wagtail 5.2
            js = ["wagtailmarkdown/js/markdown-textarea-adapter.js"]

    register(MarkdownTextareaAdapter(), MarkdownTextarea)
