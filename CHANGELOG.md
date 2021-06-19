# Changelog

## Unreleased

## 0.7.0 - 18 June 2021

- Add test suite
- Move all options in a single setting and allow further customisations ([#82](https://github.com/torchbox/wagtail-markdown/pull/82)) - Thanks @rokdd

### 0.7.0-rc2 - 15th June 2021

- Wagtail 2.13 compatibility ([#81](https://github.com/torchbox/wagtail-markdown/pull/81))

### 0.7.0-rc1 - 28th April 2021

- Switched to using [EasyMDE](https://github.com/Ionaru/easy-markdown-editor) ([#76](https://github.com/torchbox/wagtail-markdown/pull/76)) - Thanks @StefanUlbrich
- Added support for extensions config via `WAGTAILMARKDOWN_EXTENSIONS_CONFIG` ([#77](https://github.com/torchbox/wagtail-markdown/pull/77)) - Thanks @StefanUlbrich and by extension @abrunyate
- Removed deprecations
- Added [pre-commit](https://pre-commit.com/) support
- Switched to [SemVer](https://semver.org/) and GitHub Actions
- Updated [bleach](https://github.com/mozilla/bleach) minimum version to 3.3.0

## 0.6 - 12th February 2020

- Dropped Python 2.7 support
- Fixed requirements to support Wagtail >2.0
- Allow superscript HTML tags
- Improved README

## 0.5 - 13th July 2018

- Adjust dependency of Wagtail to < 2.3
- Fix support of Wagtail 2 ([#46](https://github.com/torchbox/wagtail-markdown/pull/46)) - @johnfraney
- Fix example in the README ([#42](https://github.com/torchbox/wagtail-markdown/pull/42)) - @benjaoming

### 0.5a3 - 26th March 2018

- Whitelist `<hr>` and `<br>` tags ([#33](https://github.com/torchbox/wagtail-markdown/pull/33)) - @tm-kn
- Fix compatibility for markdown panel in Wagtail 2.0 ([#37](https://github.com/torchbox/wagtail-markdown/pull/37)) - @rspeed

### 0.5a2 - 14th February 2018

- Update simplemde to 1.11.2 ([#31](https://github.com/torchbox/wagtail-markdown/pull/31)) - @stuaxo
- Update imports to work with Wagtail 2.0 ([#31](https://github.com/torchbox/wagtail-markdown/pull/31)) - @stuaxo
- Fix packaging issues so static files are included in PyPI

### 0.5a1 - 7th December 2017

- Fix problem with app loading
- Make it compatible with newer versions of Wagtail that require `context` parameters in blocks' `render_basic` method.
- Restructure app, refactor code. Add depreciation warnings.
