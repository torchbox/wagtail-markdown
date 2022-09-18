from django.test import TestCase

from wagtailmarkdown.edit_handlers import MarkdownPanel
from wagtailmarkdown.fields import MarkdownField
from wagtailmarkdown.warnings import WagtailMarkdownDeprecationWarning


class TestDeprecatedEditHandler(TestCase):
    def test_deprecated_edit_handler(self):
        with self.assertWarnsMessage(
            WagtailMarkdownDeprecationWarning,
            "The `wagtailmarkdown.edit_handlers.MarkdownPanel` field panel is deprecated. "
            "Please use the `FieldPanel()` instead.",
        ):

            class DeprecatedPageWithMarkdownPanel:
                body = MarkdownField(blank=True)
                content_panels = [MarkdownPanel("body")]
