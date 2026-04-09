from unittest import TestCase

from django.test import override_settings

from wagtailmarkdown.constants import DEFAULT_NH3_KWARGS, SETTINGS_MODE_OVERRIDE
from wagtailmarkdown.utils import (
    _coerce_nh3_kwargs_types,
    _get_default_markdown_kwargs,
    _get_markdown_kwargs,
    _get_nh3_kwargs,
)


WAGTAILMARKDOWN_NH3_SETTINGS = {
    "allowed_tags": ["i"],
    "allowed_styles": ["some_style"],
    "allowed_attributes": {"i": ["aria-hidden"], "a": ["data-test"]},
    "extensions": ["toc", "sane_lists"],
    "extension_configs": {
        "codehilite": [("guess_lang", True)],
        "pymdownx.arithmatex": {"generic": True},
    },
}


# def _get_expected_default_nh3_kwargs():
#     return {
#         "tags": set(DEFAULT_NH3_KWARGS["tags"]),
#         "attributes": {
#             key: set(value) for key, value in DEFAULT_NH3_KWARGS["attributes"].items()
#         },
#         "filter_style_properties": set(DEFAULT_NH3_KWARGS["filter_style_properties"]),
#     }


class TestSettings(TestCase):
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

        self.assertNotIn("toc", kwargs["extensions"])
        self.assertNotIn("pymdownx.arithmatex", kwargs["extension_configs"])
        self.assertEqual(
            kwargs["extension_configs"]["codehilite"], [("guess_lang", False)]
        )

        with override_settings(WAGTAILMARKDOWN=WAGTAILMARKDOWN_NH3_SETTINGS):
            kwargs = _get_markdown_kwargs()
            self.assertIn("toc", kwargs["extensions"])
            self.assertEqual(
                kwargs["extension_configs"]["pymdownx.arithmatex"], {"generic": True}
            )
            self.assertEqual(
                kwargs["extension_configs"]["codehilite"], [("guess_lang", True)]
            )

        with override_settings(WAGTAILMARKDOWN={"tab_length": 2}):
            kwargs = _get_markdown_kwargs()
            self.assertEqual(kwargs["tab_length"], 2)

        with override_settings(WAGTAILMARKDOWN={"extensions": ["toc"]}):
            kwargs = _get_markdown_kwargs()
            self.assertIn("toc", kwargs["extensions"])
            self.assertEqual(
                kwargs["extension_configs"], default_kwargs["extension_configs"]
            )

        with override_settings(
            WAGTAILMARKDOWN={"extension_configs": {"sane_lists": ["foo"]}}
        ):
            kwargs = _get_markdown_kwargs()
            self.assertNotIn("sane_lists", default_kwargs["extension_configs"])
            self.assertIn("sane_lists", kwargs["extension_configs"])

        OVERRIDE_MARKDOWN_SETTINGS = WAGTAILMARKDOWN_NH3_SETTINGS.copy()
        OVERRIDE_MARKDOWN_SETTINGS["extensions_settings_mode"] = SETTINGS_MODE_OVERRIDE
        OVERRIDE_MARKDOWN_SETTINGS["extension_configs"] = {
            "pymdownx.arithmatex": {"generic": True}
        }
        with override_settings(WAGTAILMARKDOWN=OVERRIDE_MARKDOWN_SETTINGS):
            kwargs = _get_markdown_kwargs()
            self.assertEqual(kwargs["extensions"], ["toc", "sane_lists"])
            self.assertEqual(
                kwargs["extension_configs"], {"pymdownx.arithmatex": {"generic": True}}
            )

    def test_bleach_options(self):
        kwargs = _get_nh3_kwargs()
        self.assertDictEqual(kwargs, _coerce_nh3_kwargs_types(DEFAULT_NH3_KWARGS))

        self.assertFalse("i" in kwargs["tags"])
        self.assertFalse("i" in kwargs["attributes"])
        self.assertFalse("some_style" in kwargs["filter_style_properties"])

        with override_settings(WAGTAILMARKDOWN=WAGTAILMARKDOWN_NH3_SETTINGS):
            kwargs = _get_nh3_kwargs()
            self.assertNotEqual(kwargs, _coerce_nh3_kwargs_types(DEFAULT_NH3_KWARGS))
            self.assertTrue("i" in kwargs["tags"])
            self.assertTrue("some_style" in kwargs["filter_style_properties"])
            self.assertEqual(kwargs["attributes"]["i"], {"aria-hidden"})
            self.assertEqual(
                sorted(kwargs["attributes"]["a"]),
                sorted(DEFAULT_NH3_KWARGS["attributes"]["a"] + ["data-test"]),
            )

    def test_get_nh3_kwargs(self):
        self.assertEqual(
            _get_nh3_kwargs(), _coerce_nh3_kwargs_types(DEFAULT_NH3_KWARGS)
        )

    def test_get_nh3_kwargs_with_styles(self):
        with override_settings(
            WAGTAILMARKDOWN={"allowed_styles": ["display", "color"]}
        ):
            self.assertListEqual(
                sorted(_get_nh3_kwargs()["filter_style_properties"]),
                sorted(
                    set(DEFAULT_NH3_KWARGS["filter_style_properties"]).union(
                        ["display", "color"]
                    )
                ),
            )
        with override_settings(
            WAGTAILMARKDOWN={
                "allowed_styles": ["display", "color"],
                "allowed_settings_mode": SETTINGS_MODE_OVERRIDE,
            }
        ):
            self.assertListEqual(
                sorted(_get_nh3_kwargs()["filter_style_properties"]),
                ["color", "display"],
            )

    def test_get_nh3_kwargs_with_tags(self):
        with override_settings(WAGTAILMARKDOWN={"allowed_tags": ["a", "iframe"]}):
            self.assertListEqual(
                sorted(_get_nh3_kwargs()["tags"]),
                sorted(set(DEFAULT_NH3_KWARGS["tags"]).union(["a", "iframe"])),
            )

        with override_settings(
            WAGTAILMARKDOWN={
                "allowed_tags": ["a", "iframe"],
                "allowed_settings_mode": SETTINGS_MODE_OVERRIDE,
            }
        ):
            self.assertListEqual(
                sorted(_get_nh3_kwargs()["tags"]),
                ["a", "iframe"],
            )

    def test_get_nh3_kwargs_with_attributes(self):
        allowed = {"*": ["data-test"]}
        with override_settings(WAGTAILMARKDOWN={"allowed_attributes": allowed}):
            expected = {
                key: list(value)
                for key, value in DEFAULT_NH3_KWARGS["attributes"].items()
            }
            expected["*"] += ["data-test"]

            attributes = _get_nh3_kwargs()["attributes"]
            for key, value in expected.items():
                self.assertListEqual(
                    sorted(value),
                    sorted(attributes[key]),
                )

        with override_settings(
            WAGTAILMARKDOWN={
                "allowed_attributes": allowed,
                "allowed_settings_mode": SETTINGS_MODE_OVERRIDE,
            }
        ):
            self.assertDictEqual(_get_nh3_kwargs()["attributes"], {"*": {"data-test"}})
