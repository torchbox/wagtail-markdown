# Changelog

## [Unreleased]

- Add tox testing for wagtail 6.2 and 6.3 and include Django 5.1
- Update the ruff github action which fixes the error seen in CI

## [0.12.1] - 2024-03-09

### Fixed

- A double `MarkdownBlock` editor initialisation issue in Wagtail 6

### Changed

- The telepath adapter code is not longer used in Wagtail 6+

## [0.12.0] - 2024-02-29

### Added

- Add Wagtail 6.0 and Django 5.0 to the test matrix ([#139](https://github.com/torchbox/wagtail-markdown/pull/139)) @katdom13, @nickmoreton
- Ability to customize tab length ([#136](https://github.com/torchbox/wagtail-markdown/pull/)) @bjackson

### Removed

- Support for Wagtail < 5.2
- The deprecated `MarkdownPanel`. Use `FieldPanel` instead.

## [0.11.1] - 2023-08-02

### Changed

- Various maintenance and tooling tweaks. Includes switching to [PyPI trusted publishing](https://docs.pypi.org/trusted-publishers/using-a-publisher/)
- Added Wagtail 5.1 to the testing matrix

## [0.11.0] - 2023-04-22

### Added

- Support for the Wagtail 5.0 dark theme

### Changed

- Minimum Wagtail requirement is 4.1 ([#120](https://github.com/torchbox/wagtail-markdown/pull/120)) Thanks @nmoreton
- Switched to using [flit](https://flit.pypa.io/en/latest/) for packaging and [ruff](https://beta.ruff.rs/docs/) for linting
- Upgraded EasyMde to v2.18.0

## [0.10.0] - 2022-09-18

### Added

- Ability to pass custom options to the EasyMDE editor ([#104](https://github.com/torchbox/wagtail-markdown/pull/104)) Thanks @frcroth
- Support for inline links and images ([#107](https://github.com/torchbox/wagtail-markdown/pull/107)). With belated thanks to @richtier for the original PR (#44)
- New settings: `allowed_settings_mode` and `extensions_settins_mode` to control the `allowed_*` and `extension*` settings mode.
  Defaults to `extend`, but you can set to `override` to override the defaults. ([#108](https://github.com/torchbox/wagtail-markdown/pull/108))

### Removed

- The custom tables extension. This means tables will no longer have the `wftable` class added to them.

## [0.9.0] - 2022-07-01

### Changed

- `wagtailmarkdown.edit_handlers.MarkdownPanel` is deprecated and will be removed in the next minor version.
  Use the Wagtail core `FieldPanel` instead.
- Updated the easymde/codemirror setup logic.

### Removed

- Dropped support for Wagtail < 2.15
- Removed long deprecated `wagtailmarkdown.fields.MarkdownBlock` import

## [0.8.0] - 2022-02-25

### Added
- Add Wagtail 2.16 and Django 4.0 compatibility ([#94](https://github.com/torchbox/wagtail-markdown/pull/94))
- Update to EasyMDE 2.16.1 ([#95](https://github.com/torchbox/wagtail-markdown/pull/95))

### Fixed
- Fix etree deprecation warnings (for `Markdown >= 3.2`) ([#93](https://github.com/torchbox/wagtail-markdown/pull/93)) - Thanks @nickmoreton
- Fix pygments code highlighting instructions ([#87](https://github.com/torchbox/wagtail-markdown/pull/87)) - Thanks @elcuy

## [0.7.0] - 2021-06-18

- Add test suite
- Move all options in a single setting and allow further customisations ([#82](https://github.com/torchbox/wagtail-markdown/pull/82)) - Thanks @rokdd

### 0.7.0-rc2 - 2021-06-15

- Wagtail 2.13 compatibility ([#81](https://github.com/torchbox/wagtail-markdown/pull/81))

### 0.7.0-rc1 - 2021-04-28

- Switched to using [EasyMDE](https://github.com/Ionaru/easy-markdown-editor) ([#76](https://github.com/torchbox/wagtail-markdown/pull/76)) - Thanks @StefanUlbrich
- Added support for extensions config via `WAGTAILMARKDOWN_EXTENSIONS_CONFIG` ([#77](https://github.com/torchbox/wagtail-markdown/pull/77)) - Thanks @StefanUlbrich and by extension @abrunyate
- Removed deprecations
- Added [pre-commit](https://pre-commit.com/) support
- Switched to [SemVer](https://semver.org/) and GitHub Actions
- Updated [bleach](https://github.com/mozilla/bleach) minimum version to 3.3.0

## [0.6] - 2020-02-12

- Dropped Python 2.7 support
- Fixed requirements to support Wagtail >2.0
- Allow superscript HTML tags
- Improved README

## [0.5] - 2018-07-13

- Adjust dependency of Wagtail to < 2.3
- Fix support of Wagtail 2 ([#46](https://github.com/torchbox/wagtail-markdown/pull/46)) - @johnfraney
- Fix example in the README ([#42](https://github.com/torchbox/wagtail-markdown/pull/42)) - @benjaoming

### 0.5a3 - 2018-03-26

- Whitelist `<hr>` and `<br>` tags ([#33](https://github.com/torchbox/wagtail-markdown/pull/33)) - @tm-kn
- Fix compatibility for markdown panel in Wagtail 2.0 ([#37](https://github.com/torchbox/wagtail-markdown/pull/37)) - @rspeed

### 0.5a2 - 2018-02-14

- Update simplemde to 1.11.2 ([#31](https://github.com/torchbox/wagtail-markdown/pull/31)) - @stuaxo
- Update imports to work with Wagtail 2.0 ([#31](https://github.com/torchbox/wagtail-markdown/pull/31)) - @stuaxo
- Fix packaging issues so static files are included in PyPI

### 0.5a1 - 2017-12-7

- Fix problem with app loading
- Make it compatible with newer versions of Wagtail that require `context` parameters in blocks' `render_basic` method.
- Restructure app, refactor code. Add depreciation warnings.


[unreleased]: https://github.com/torchbox/wagtail-markdown/compare/v0.12.1...HEAD
[0.12.1]: https://github.com/torchbox/wagtail-markdown/compare/v0.12.0...v0.12.1
[0.12.0]: https://github.com/torchbox/wagtail-markdown/compare/v0.11.0...v0.12.0
[0.11.1]: https://github.com/torchbox/wagtail-markdown/compare/v0.11.0...v0.11.1
[0.11.0]: https://github.com/torchbox/wagtail-markdown/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/torchbox/wagtail-markdown/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/torchbox/wagtail-markdown/compare/0.8.0...v0.9.0
[0.8.0]: https://github.com/torchbox/wagtail-markdown/compare/0.7.0...0.8.0
[0.7.0]: https://github.com/torchbox/wagtail-markdown/compare/0.6...0.7.0
[0.6]: https://github.com/torchbox/wagtail-markdown/compare/0.5...0.6
[0.5]: https://github.com/torchbox/wagtail-markdown/compare/038a0e5...0.5
