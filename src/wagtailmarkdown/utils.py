from collections import defaultdict

import bleach
import markdown

from django.conf import settings
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe

from wagtailmarkdown.constants import DEFAULT_BLEACH_KWARGS, SETTINGS_MODE_OVERRIDE
from wagtailmarkdown.mdx.inlinepatterns import ImageExtension, LinkExtension
from wagtailmarkdown.mdx.linker import LinkerExtension


def render_markdown(text, context=None):
    """
    Turn markdown into HTML.
    """
    markdown_html = _transform_markdown_into_html(text)
    sanitised_markdown_html = _sanitise_markdown_html(markdown_html)
    # note: we use mark_safe here because bleach is already sanitising the HTML
    return mark_safe(sanitised_markdown_html)  # noqa: S308


def _transform_markdown_into_html(text):
    return markdown.markdown(smart_str(text), **_get_markdown_kwargs())


def _sanitise_markdown_html(markdown_html):
    return bleach.clean(markdown_html, **_get_bleach_kwargs())


def _get_bleach_kwargs():
    bleach_kwargs = DEFAULT_BLEACH_KWARGS.copy()

    if not hasattr(settings, "WAGTAILMARKDOWN"):
        return bleach_kwargs

    override = (
        settings.WAGTAILMARKDOWN.get("allowed_settings_mode", "extend").lower()
        == SETTINGS_MODE_OVERRIDE
    )
    if "allowed_styles" in settings.WAGTAILMARKDOWN:
        if override:
            bleach_kwargs["styles"] = settings.WAGTAILMARKDOWN["allowed_styles"]
        else:
            bleach_kwargs["styles"] = list(
                set(
                    settings.WAGTAILMARKDOWN["allowed_styles"] + bleach_kwargs["styles"]
                )
            )
    if "allowed_tags" in settings.WAGTAILMARKDOWN:
        if override:
            bleach_kwargs["tags"] = settings.WAGTAILMARKDOWN["allowed_tags"]
        else:
            bleach_kwargs["tags"] = list(
                set(settings.WAGTAILMARKDOWN["allowed_tags"] + bleach_kwargs["tags"])
            )

    if "allowed_attributes" in settings.WAGTAILMARKDOWN:
        if override:
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
    kwargs = {
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

    return kwargs


def _get_markdown_kwargs():
    kwargs = _get_default_markdown_kwargs()

    if not hasattr(settings, "WAGTAILMARKDOWN"):
        return kwargs

    markdown_settings = settings.WAGTAILMARKDOWN
    override = (
        markdown_settings.get("extensions_settings_mode", "extend").lower()
        == SETTINGS_MODE_OVERRIDE
    )
    if "extensions" in markdown_settings:
        if override:
            kwargs["extensions"] = markdown_settings["extensions"]
        else:
            kwargs["extensions"] = list(
                set(kwargs["extensions"] + markdown_settings["extensions"])
            )

    if "extension_configs" in markdown_settings:
        if override:
            kwargs["extension_configs"] = markdown_settings["extension_configs"]
        else:
            kwargs["extension_configs"].update(markdown_settings["extension_configs"])

    if "tab_length" in markdown_settings:
        kwargs["tab_length"] = markdown_settings["tab_length"]

    return kwargs
