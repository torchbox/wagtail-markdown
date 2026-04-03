from collections import defaultdict
from copy import deepcopy

import markdown
import nh3

from django.conf import settings
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe

from wagtailmarkdown.constants import DEFAULT_NH3_KWARGS, SETTINGS_MODE_OVERRIDE
from wagtailmarkdown.mdx.inlinepatterns import (
    DelExtension,
    ImageExtension,
    LinkExtension,
)
from wagtailmarkdown.mdx.linker import LinkerExtension


def render_markdown(text, context=None):
    """
    Turn markdown into HTML.
    """
    markdown_html = _transform_markdown_into_html(text)
    sanitised_markdown_html = _sanitise_markdown_html(markdown_html)
    # note: we use mark_safe here because nh3 is already sanitising the HTML
    return mark_safe(sanitised_markdown_html)  # noqa: S308


def _transform_markdown_into_html(text):
    return markdown.markdown(smart_str(text), **_get_markdown_kwargs())


def _sanitise_markdown_html(markdown_html):
    nh3_kwargs = _get_nh3_kwargs()
    nh3_kwargs["tags"] = set(nh3_kwargs["tags"])
    nh3_kwargs["attributes"] = {
        key: set(value) for key, value in nh3_kwargs["attributes"].items()
    }
    nh3_kwargs["filter_style_properties"] = set(nh3_kwargs["filter_style_properties"])
    return nh3.clean(markdown_html, **nh3_kwargs)


def _get_nh3_kwargs():
    nh3_kwargs = deepcopy(DEFAULT_NH3_KWARGS)

    if not hasattr(settings, "WAGTAILMARKDOWN"):
        return nh3_kwargs

    override = (
        settings.WAGTAILMARKDOWN.get("allowed_settings_mode", "extend").lower()
        == SETTINGS_MODE_OVERRIDE
    )
    if "allowed_styles" in settings.WAGTAILMARKDOWN:
        if override:
            nh3_kwargs["filter_style_properties"] = settings.WAGTAILMARKDOWN[
                "allowed_styles"
            ]
        else:
            nh3_kwargs["filter_style_properties"] = list(
                set(
                    settings.WAGTAILMARKDOWN["allowed_styles"]
                    + nh3_kwargs["filter_style_properties"]
                )
            )
    if "allowed_tags" in settings.WAGTAILMARKDOWN:
        if override:
            nh3_kwargs["tags"] = list(settings.WAGTAILMARKDOWN["allowed_tags"])
        else:
            nh3_kwargs["tags"] = list(
                dict.fromkeys(
                    nh3_kwargs["tags"] + settings.WAGTAILMARKDOWN["allowed_tags"]
                )
            )

    if "allowed_attributes" in settings.WAGTAILMARKDOWN:
        if override:
            nh3_kwargs["attributes"] = settings.WAGTAILMARKDOWN["allowed_attributes"]
        else:
            merged = defaultdict(set)
            for _dict in [
                nh3_kwargs["attributes"],
                settings.WAGTAILMARKDOWN["allowed_attributes"],
            ]:
                for key, value in _dict.items():
                    merged[key].update(value)
            nh3_kwargs["attributes"] = {
                key: list(value) for key, value in merged.items()
            }

    return nh3_kwargs


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
            DelExtension(),
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
