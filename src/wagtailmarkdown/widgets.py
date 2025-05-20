from django import forms
from django.conf import settings
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
