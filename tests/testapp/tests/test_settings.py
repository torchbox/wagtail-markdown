from unittest import TestCase

from django.test import override_settings

from wagtailmarkdown.utils import (
    _get_bleach_kwargs,
    _get_default_bleach_kwargs,
    _get_default_markdown_kwargs,
    _get_markdown_kwargs,
)

WAGTAILMARKDOWN_BLEACH_SETTINGS = {
    "allowed_tags": ["i"],
    "allowed_styles": ["some_style"],
    "allowed_attributes": {"i": ["aria-hidden"], "a": ["data-test"]},
    "extensions": ["toc", "sane_lists"],
    "extension_configs": {
        "codehilite": [("guess_lang", True)],
        "pymdownx.arithmatex": {"generic": True},
    },
}


class TestSettings(TestCase):
    def test_bleach_options(self):
        kwargs = _get_bleach_kwargs()
        self.assertDictEqual(kwargs, _get_default_bleach_kwargs())

        self.assertFalse("i" in kwargs["tags"])
        self.assertFalse("i" in kwargs["attributes"])
        self.assertFalse("some_style" in kwargs["styles"])

        with override_settings(WAGTAILMARKDOWN=WAGTAILMARKDOWN_BLEACH_SETTINGS):
            kwargs = _get_bleach_kwargs()
            self.assertNotEqual(kwargs, _get_default_bleach_kwargs())
            self.assertTrue("i" in kwargs["tags"])
            self.assertTrue("some_style" in kwargs["styles"])
            self.assertEqual(kwargs["attributes"]["i"], ["aria-hidden"])
            self.assertEqual(kwargs["attributes"]["a"], ["data-test"])

    def test_markdown_kwargs(self):
        kwargs = _get_markdown_kwargs()
        default_kwargs = _get_default_markdown_kwargs()

        self.assertEqual(len(kwargs["extensions"]), len(default_kwargs["extensions"]))
        self.assertEqual(kwargs["extensions"][0:2], default_kwargs["extensions"][0:2])
        # the rest of the default options are instances of classes
        for index, extension in enumerate(kwargs["extensions"][2:], start=2):
            self.assertEqual(type(extension), type(default_kwargs["extensions"][index]))

        self.assertEqual(
            kwargs["extension_configs"], default_kwargs["extension_configs"]
        )

        self.assertFalse("toc" in kwargs["extensions"])
        self.assertFalse("pymdownx.arithmatex" in kwargs["extension_configs"])
        self.assertEqual(
            kwargs["extension_configs"]["codehilite"], [("guess_lang", False)]
        )

        with override_settings(WAGTAILMARKDOWN=WAGTAILMARKDOWN_BLEACH_SETTINGS):
            kwargs = _get_markdown_kwargs()
            self.assertTrue("toc" in kwargs["extensions"])
            self.assertEqual(
                kwargs["extension_configs"]["pymdownx.arithmatex"], {"generic": True}
            )
            self.assertEqual(
                kwargs["extension_configs"]["codehilite"], [("guess_lang", True)]
            )
