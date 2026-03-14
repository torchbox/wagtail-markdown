from collections import defaultdict

import nh3
import markdown

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
    return nh3.clean(markdown_html, **_get_nh3_kwargs())


def _get_nh3_kwargs():
    nh3_kwargs = DEFAULT_NH3_KWARGS.copy()

    if not hasattr(settings, "WAGTAILMARKDOWN"):
        return nh3_kwargs

    override = (
        settings.WAGTAILMARKDOWN.get("allowed_settings_mode", "extend").lower()
        == SETTINGS_MODE_OVERRIDE
    )
    if "allowed_styles" in settings.WAGTAILMARKDOWN:
        if override:
            nh3_kwargs["filter_style_properties"] = set(settings.WAGTAILMARKDOWN["allowed_styles"])
        else:
            nh3_kwargs["filter_style_properties"] = set(
                list(nh3_kwargs.get("filter_style_properties", set())) + settings.WAGTAILMARKDOWN["allowed_styles"]
            )
    if "allowed_tags" in settings.WAGTAILMARKDOWN:
        if override:
            nh3_kwargs["tags"] = set(settings.WAGTAILMARKDOWN["allowed_tags"])
        else:
            nh3_kwargs["tags"] = set(
                list(nh3_kwargs.get("tags", set())) + settings.WAGTAILMARKDOWN["allowed_tags"]
            )

    if "allowed_attributes" in settings.WAGTAILMARKDOWN:
        if override:
            nh3_kwargs["attributes"] = dict((k, set(v)) for k, v in settings.WAGTAILMARKDOWN["allowed_attributes"].items())
        else:
            # Convert nh3 default attributes to same format as user attributes
            default_attrs = nh3_kwargs.get("attributes", {})
            if default_attrs and isinstance(next(iter(default_attrs.values())), set):
                # Already in set format
                user_attrs = settings.WAGTAILMARKDOWN["allowed_attributes"]
            else:
                # Convert from list format to set format
                default_attrs = {k: set(v) for k, v in default_attrs.items()}
                user_attrs = {k: set(v) for k, v in settings.WAGTAILMARKDOWN["allowed_attributes"].items()}
            
            # Merge attributes
            merged = defaultdict(set)
            for _dict in [default_attrs, user_attrs]:
                for key, value in _dict.items():
                    merged[key].update(value)
            nh3_kwargs["attributes"] = {key: value for key, value in merged.items()}

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
