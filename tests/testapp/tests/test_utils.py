from django.test import TestCase, override_settings

from wagtailmarkdown.constants import DEFAULT_BLEACH_KWARGS
from wagtailmarkdown.utils import _get_bleach_kwargs


class UtilsTests(TestCase):
    def test_get_bleach_kwargs(self):
        self.assertEqual(_get_bleach_kwargs(), DEFAULT_BLEACH_KWARGS)

    @override_settings(WAGTAILMARKDOWN={"allowed_styles": ["display", "color"]})
    def test_get_bleach_kwargs_with_additional_styles(self):
        default_styles = DEFAULT_BLEACH_KWARGS["styles"]
        self.assertListEqual(
            sorted(_get_bleach_kwargs()["styles"]),
            sorted(set(default_styles + ["display", "color"])),
        )

    @override_settings(WAGTAILMARKDOWN={"allowed_tags": ["a", "iframe"]})
    def test_get_bleach_kwargs_with_additional_tags(self):
        default_tags = DEFAULT_BLEACH_KWARGS["tags"]
        self.assertListEqual(
            sorted(_get_bleach_kwargs()["tags"]),
            sorted(set(default_tags + ["a", "iframe"])),
        )
