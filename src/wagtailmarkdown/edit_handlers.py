import warnings

from wagtail import VERSION as WAGTAIL_VERSION


if WAGTAIL_VERSION >= (3, 0):
    from wagtail.admin.panels import FieldPanel
else:
    from wagtail.admin.edit_handlers import FieldPanel

from wagtailmarkdown.warnings import WagtailMarkdownDeprecationWarning


class MarkdownPanel(FieldPanel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        warnings.warn(
            (
                "The `wagtailmarkdown.edit_handlers.MarkdownPanel` field panel is deprecated. "
                "Please use the `FieldPanel()` instead."
            ),
            WagtailMarkdownDeprecationWarning,
            stacklevel=2,
        )
