from collections import defaultdict

from django.conf import settings
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe

import bleach
import markdown

from wagtailmarkdown.constants import DEFAULT_BLEACH_KWARGS, SETTINGS_MODE_REPLACE
from wagtailmarkdown.mdx.inlinepatterns import ImageExtension, LinkExtension
from wagtailmarkdown.mdx.linker import LinkerExtension


def render_markdown(text, context=None):
    """
    Turn markdown into HTML.
    """
    markdown_html = _transform_markdown_into_html(text)
    sanitised_markdown_html = _sanitise_markdown_html(markdown_html)
    return mark_safe(sanitised_markdown_html)


def _transform_markdown_into_html(text):
    return markdown.markdown(smart_str(text), **_get_markdown_kwargs())


def _sanitise_markdown_html(markdown_html):
    return bleach.clean(markdown_html, **_get_bleach_kwargs())


def _get_bleach_kwargs():
    bleach_kwargs = DEFAULT_BLEACH_KWARGS.copy()

    if not hasattr(settings, "WAGTAILMARKDOWN"):
        return bleach_kwargs

    replace = (
        settings.WAGTAILMARKDOWN.get("allowed_settings_mode", "extend").lower()
        == SETTINGS_MODE_REPLACE
    )
    if "allowed_styles" in settings.WAGTAILMARKDOWN:
        if replace:
            bleach_kwargs["styles"] = settings.WAGTAILMARKDOWN["allowed_styles"]
        else:
            bleach_kwargs["styles"] = list(
                set(
                    settings.WAGTAILMARKDOWN["allowed_styles"] + bleach_kwargs["styles"]
                )
            )
    if "allowed_tags" in settings.WAGTAILMARKDOWN:
        if replace:
            bleach_kwargs["tags"] = settings.WAGTAILMARKDOWN["allowed_tags"]
        else:
            bleach_kwargs["tags"] = list(
                set(settings.WAGTAILMARKDOWN["allowed_tags"] + bleach_kwargs["tags"])
            )

    if "allowed_attributes" in settings.WAGTAILMARKDOWN:
        if replace:
            bleach_kwargs["attributes"] = settings.WAGTAILMARKDOWN["allowed_attributes"]
        else:
            merged = defaultdict(set)
            for _dict in [
                bleach_kwargs["attributes"],
                settings.WAGTAILMARKDOWN["allowed_attributes"],
            ]:
                for key, value in _dict.items():
                    merged[key].update(value)
            bleach_kwargs["attributes"] = {
                key: list(value) for key, value in merged.items()
            }

    return bleach_kwargs


def _get_default_markdown_kwargs():
    markdown_kwargs = {
        "extensions": [
            "extra",
            "codehilite",
            "tables",
            LinkerExtension(
                {
                    "__default__": "wagtailmarkdown.mdx.linkers.page",
                    "page:": "wagtailmarkdown.mdx.linkers.page",
                    "image:": "wagtailmarkdown.mdx.linkers.image",
                    "doc:": "wagtailmarkdown.mdx.linkers.document",
                }
            ),
            LinkExtension(),
            ImageExtension(),
        ],
        "extension_configs": {
            "codehilite": [
                ("guess_lang", False),
            ]
        },
        "output_format": "html5",
    }

    return markdown_kwargs


def _get_markdown_kwargs():
    markdown_kwargs = _get_default_markdown_kwargs()

    if (
        hasattr(settings, "WAGTAILMARKDOWN")
        and "extensions" in settings.WAGTAILMARKDOWN
    ):
        markdown_kwargs["extensions"] = list(
            set(markdown_kwargs["extensions"] + settings.WAGTAILMARKDOWN["extensions"])
        )

    if (
        hasattr(settings, "WAGTAILMARKDOWN")
        and "extension_configs" in settings.WAGTAILMARKDOWN
    ):
        markdown_kwargs["extension_configs"].update(
            settings.WAGTAILMARKDOWN["extension_configs"]
        )

    return markdown_kwargs
