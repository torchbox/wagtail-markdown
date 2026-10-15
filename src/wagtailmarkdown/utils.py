import re

from collections import defaultdict
from copy import deepcopy

import markdown
import nh3

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import smart_str
from django.utils.safestring import mark_safe
from wagtail.images.exceptions import InvalidFilterSpecError
from wagtail.images.shortcuts import get_rendition_or_not_found

from wagtailmarkdown.constants import DEFAULT_NH3_KWARGS, SETTINGS_MODE_OVERRIDE
from wagtailmarkdown.mdx.linker import LinkerExtension


def render_markdown(text, context=None):
    """
    Turn markdown into HTML.
    """
    md = markdown.Markdown(**_get_markdown_kwargs())
    markdown_html = md.convert(smart_str(text))
    markdown_html = _unwrap_image_placeholders(markdown_html, md)
    sanitised_markdown_html = _sanitise_markdown_html(markdown_html)
    sanitised_markdown_html = _render_image_placeholders(sanitised_markdown_html, md)
    # note: we use mark_safe here because nh3 is already sanitising the HTML,
    # and images rendered with the `image_template` setting come from a template
    return mark_safe(sanitised_markdown_html)  # noqa: S308


def _unwrap_image_placeholders(html, md):
    """
    Turn the empty elements Markdown leaves for images by the `image_template`
    setting into plain text placeholders, which survive sanitising.
    """
    images = getattr(md, "wagtailmarkdown_images", None)
    if images is None or not images.items:
        return html

    token = re.escape(images.token)
    return re.sub(rf"<({token}\d+)></\1>", r"\1", html)


def _render_image_placeholders(html, md):
    """
    Replace the placeholders left for images by the `image_template` setting
    with the rendered template. A placeholder that is the only content of its
    paragraph replaces the paragraph, with `standalone` set in the context.
    """
    images = getattr(md, "wagtailmarkdown_images", None)
    if images is None or not images.items:
        return html

    def render(match, *, standalone):
        item = images.items[int(match.group(1))]
        return _render_image(item, images.template_name, standalone=standalone)

    token = re.escape(images.token)
    html = re.sub(
        rf"<p>\s*{token}(\d+)\s*</p>",
        lambda m: render(m, standalone=True),
        html,
    )
    return re.sub(rf"{token}(\d+)", lambda m: render(m, standalone=False), html)


def _render_image(item, template_name, *, standalone):
    image = item.image
    # The same attributes Wagtail's ImageBlock sets, which renditions use
    # for their alt text, in {% image %}, {% picture %} and img_tag().
    image.contextual_alt_text = item.alt
    image.decorative = not item.alt

    rendition = None
    if item.filter_spec:
        try:
            rendition = get_rendition_or_not_found(image, item.filter_spec)
        except InvalidFilterSpecError:
            rendition = None

    # Stripped, so an image inside text adds no spaces around itself.
    return render_to_string(
        template_name,
        {
            "image": image,
            "alt": item.alt,
            "class": item.css_class,
            "caption": item.caption,
            "rendition": rendition,
            "standalone": standalone,
        },
    ).strip()


def _sanitise_markdown_html(markdown_html):
    nh3_kwargs = _get_nh3_kwargs()
    return nh3.clean(markdown_html, **nh3_kwargs)


def _coerce_nh3_kwargs_types(nh3_kwargs):
    coerced = deepcopy(nh3_kwargs)
    coerced["tags"] = set(coerced["tags"])
    coerced["attributes"] = {
        key: set(value) for key, value in coerced["attributes"].items()
    }
    coerced["filter_style_properties"] = set(coerced["filter_style_properties"])

    return coerced


def _get_nh3_kwargs():
    nh3_kwargs = deepcopy(DEFAULT_NH3_KWARGS)

    if not hasattr(settings, "WAGTAILMARKDOWN"):
        return _coerce_nh3_kwargs_types(nh3_kwargs)

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
    if "link_rel" in settings.WAGTAILMARKDOWN:
        nh3_kwargs["link_rel"] = settings.WAGTAILMARKDOWN["link_rel"]

    return _coerce_nh3_kwargs_types(nh3_kwargs)


def _get_default_markdown_kwargs():
    # imported inline to avoid AppRegistryNotReady exceptions
    from wagtailmarkdown.mdx.inlinepatterns import (
        DelExtension,
        ImageExtension,
        LinkExtension,
    )

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
            ImageExtension(template_name=_get_image_template()),
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


def _get_image_template():
    return getattr(settings, "WAGTAILMARKDOWN", {}).get("image_template")


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
