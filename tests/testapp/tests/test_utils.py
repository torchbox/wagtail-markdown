from django.test import TestCase, override_settings

from wagtailmarkdown.utils import _get_bleach_kwargs, _get_default_bleach_kwargs


class UtilsTests(TestCase):
    def test_get_bleach_kwargs(self):
        self.assertEqual(_get_bleach_kwargs(), _get_default_bleach_kwargs())

    @override_settings(WAGTAILMARKDOWN={"allowed_styles": ["display", "color"]})
    def test_get_bleach_kwargs_with_additional_styles(self):
        default_styles = _get_default_bleach_kwargs()["styles"]
        self.assertListEqual(
            sorted(_get_bleach_kwargs()["styles"]),
            sorted(set(default_styles + ["display", "color"])),
        )

    @override_settings(WAGTAILMARKDOWN={"allowed_tags": ["a", "iframe"]})
    def test_get_bleach_kwargs_with_additional_tags(self):
        default_tags = _get_default_bleach_kwargs()["tags"]
        self.assertListEqual(
            sorted(_get_bleach_kwargs()["tags"]),
            sorted(set(default_tags + ["a", "iframe"])),
        )
