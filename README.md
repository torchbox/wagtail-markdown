## wagtail-markdown: Markdown fields and blocks for Wagtail

[![Build status](https://img.shields.io/github/actions/workflow/status/torchbox/wagtail-markdown/ci.yml?branch=main)](https://github.com/torchbox/wagtail-markdown/actions)
[![PyPI](https://img.shields.io/pypi/v/wagtail-markdown.svg)](https://pypi.org/project/wagtail-markdown/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/torchbox/wagtail-markdown/main.svg)](https://results.pre-commit.ci/latest/github/torchbox/wagtail-markdown/main)


Tired of annoying rich text editors getting in the way of your content
input?  Wish Wagtail worked more like a wiki?  Well, now it can.

`wagtail-markdown` provides Markdown field support for [Wagtail](https://github.com/torchbox/wagtail/).
Specifically, it provides:

* A `wagtailmarkdown.blocks.MarkdownBlock` for use in StreamFields.
* A `wagtailmarkdown.fields.MarkdownField` for use in Page models.
* A `markdown` template tag.

The markdown rendered is based on `python-markdown`, but with several
extensions to make it actually useful in Wagtail:

* [Code highlighting](#syntax-highlighting).
* [Inline links](#inline-links).
* Inline Markdown preview using [EasyMDE](https://github.com/Ionaru/easy-markdown-editor)
* Tables

These are implemented using the `python-markdown` extension interface.

### Installation
Available on PyPI - https://pypi.org/project/wagtail-markdown/.

Install using pip (`pip install wagtail-markdown`), poetry (`poetry add wagtail-markdown`) or your package manager of choice.

After installing the package, add `wagtailmarkdown` to the list of installed apps in your settings file:

```python
# settings.py

INSTALLED_APPS = [
    # ...
    "wagtailmarkdown",
]
```

### Configuration

All `wagtail-markdown` settings are defined in a single `WAGTAILMARKDOWN` dictionary in your settings file:

```python
# settings.py

WAGTAILMARKDOWN = {
    "autodownload_fontawesome": False,
    "allowed_tags": [],  # optional. a list of HTML tags. e.g. ['div', 'p', 'a']
    "allowed_styles": [],  # optional. a list of styles
    "allowed_attributes": {},  # optional. a dict with HTML tag as key and a list of attributes as value
    "allowed_settings_mode": "extend",  # optional. Possible values: "extend" or "override". Defaults to "extend".
    "extensions": [],  # optional. a list of python-markdown supported extensions
    "extension_configs": {},  # optional. a dictionary with the extension name as key, and its configuration as value
    "extensions_settings_mode": "extend",  # optional. Possible values: "extend" or "override". Defaults to "extend".
    "tab_length": 4,  # optional. Sets the length of tabs used by python-markdown to render the output. This is the number of spaces used to replace with a tab character. Defaults to 4.
}
```

Note: `allowed_tags`, `allowed_styles`, `allowed_attributes`, `extensions` and `extension_configs` are added to the
[default wagtail-markdown settings](https://github.com/torchbox/wagtail-markdown/blob/main/src/wagtailmarkdown/constants.py).


#### Custom FontAwesome Configuration - `autodownload_fontawesome`
The EasyMDE editor is compatible with [FontAwesome 5](https://fontawesome.com/how-to-use/graphql-api/intro/getting-started).
By default, EasyMDE will get version 4.7.0 from a CDN. To specify your own version, set

```python
# settings.py

WAGTAILMARKDOWN = {
    # ...
    "autodownload_fontawesome": False,
}
```

Get the desired FontAwesome version. For the latest version you can use:

```sh
curl -H "Content-Type: application/json" \
-d '{ "query": "query { release(version: \"latest\") { version } }" }' \
https://api.fontawesome.com
```

then add the following to a `wagtail_hooks` module in a registered app in your application:

```python
# Content of app_name/wagtail_hooks.py
from wagtail import hooks
from django.conf import settings
from django.utils.html import format_html


@hooks.register("insert_global_admin_css")
def import_fontawesome_stylesheet():
    elem = '<link rel="stylesheet" href="{}path/to/font-awesome.min.css">'.format(
        settings.STATIC_URL
    )
    return format_html(elem)
```

Note that due to the way EasyMDE defines the toolbar icons it is not compatible with
[Wagtail FontAwesome](https://gitlab.com/alexgleason/wagtailfontawesome)

##### Using with django-compressor

You may have your own SCSS sources that you want to precompile on the fly.
We can invoke django-compressor to fetch our Font Awesome SCSS sources like this:

```python
# Content of app_name/wagtail_hooks.py
from compressor.css import CssCompressor
from wagtail import hooks
from django.conf import settings
from django.utils.html import format_html


@hooks.register("insert_global_admin_css")
def import_fontawesome_stylesheet():
    elem = '<link rel="stylesheet" type="text/x-scss" href="{}scss/fontawesome.scss">'.format(
        settings.STATIC_URL
    )
    compressor = CssCompressor("css", content=elem)
    output = ""
    for s in compressor.hunks():
        output += s
    return format_html(output)
```


#### Markdown extensions - `extensions`/`extension_configs`

You can configure wagtail-markdown to use additional Markdown extensions using the `extensions` setting.

For example, to enable the [Table of Contents](https://python-markdown.github.io/extensions/toc/) and
[Sane Lists](https://python-markdown.github.io/extensions/sane_lists/) extensions:

```python
WAGTAILMARKDOWN = {
    # ...
    "extensions": ["toc", "sane_lists"]
}
```

Extensions can be configured too:

```python
WAGTAILMARKDOWN = {
    # ...
    "extension_configs": {"pymdownx.arithmatex": {"generic": True}}
}
```

#### Allowed HTML - `allowed_styles` / `allowed_attributes` / `allowed_tags`

wagtail-markdown uses [bleach](https://github.com/mozilla/bleach) to sanitise the input. To extend the default
bleach configurations, you can add your own allowed tags, styles or attributes:

```python
WAGTAILMARKDOWN = {
    # ...
    "allowed_tags": ["i"],
    "allowed_styles": ["some_style"],
    "allowed_attributes": {"i": ["aria-hidden"]},
}
```

#### Syntax highlighting

Syntax highlighting using codehilite is an optional feature, which works by
adding CSS classes to the generated HTML. To use these classes, you will need
to install Pygments (`pip install Pygments`), and to generate an appropriate
stylesheet. You can generate one as per the [Pygments documentation](http://pygments.org/docs/quickstart/), with:

```python
from pygments.formatters import HtmlFormatter

print(HtmlFormatter().get_style_defs(".codehilite"))
```

Save the output to a file and reference it somewhere that will be
picked up on pages rendering the relevant output, e.g. your base template:

```html+django
<link rel="stylesheet" type="text/css" href="{% static 'path/to/pygments.css' %}">
```

#### EasyMDE configuration

You can customise the [EasyMDE options](https://github.com/Ionaru/easy-markdown-editor#configuration). To do this,
create a JavaScript file in your app (for example `my_app_name/static/js/easymde_custom.js`) and add the following:

```js
window.wagtailMarkdown = window.wagtailMarkdown || {};
window.wagtailMarkdown.options = window.wagtailMarkdown.options || {};
window.wagtailMarkdown.options.spellChecker = false;
```

This overrides a specific option and leaves any other ones untouched. If you want to override all options, you can do:

```js
window.wagtailMarkdown = window.wagtailMarkdown || {};
window.wagtailMarkdown.options = {
    spellChecker: false,
}
```

To make sure that your JavaScript is executed, create a hook in `my_app_name/wagtail_hooks.py`:

```python
from django.templatetags.static import static
from django.utils.html import format_html

from wagtail import hooks


@hooks.register("insert_global_admin_js", order=100)
def global_admin_js():
    """Add /static/js/admin/easymde_custom.js to the admin."""
    return format_html('<script src="{}"></script>', static("js/easymde_custom.js"))
```

#### Inline links

wagtail-markdown supports custom inline links syntax:

| Link to                                | Syntax                                                              | Notes                                                                                                                                                                |
|----------------------------------------|---------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Pages                                  | `[title](page:PAGE_ID)`                                             | `PAGE_ID` is the page ID                                                                                                                                             |
| Documents                              | `[title](doc:DOCUMENT_ID)`                                          | `DOCUMENT_ID` is the document ID                                                                                                                                     |
| Media                                  | `[title](media:MEDIA_ID)`                                           | Needs [wagtailmedia](https://github.com/torchbox/wagtailmedia). `MEDIA_ID` is the media item ID                                                                      |
| Images                                 | `![alt text](image:IMAGE_ID)`                                       | Renders an image tag. `IMAGE_ID` is the image ID                                                                                                                     |
| ↳ with class attribute                 | `![alt text](image:IMAGE_ID,class=the-class-name)`                  | adds `class="the-class-name" to the `<img>` tag                                                                                                                      |
| ↳ with rendition filter                | `![alt text](image:IMAGE_ID,filter=fill-200x200&#x7c;format-webp)`  | Uses the same format as [generating renditions in Python](https://docs.wagtail.org/en/stable/advanced_topics/images/renditions.html#generating-renditions-in-python) |
| ↳ class name and filter can be stacked | `![alt text](image:IMAGE_ID,class=the-class-name,filter=width-100)` |                                                                                                                                                                      |



Previously we supported custom link tags that used the target object title. They had the following form:
* `<:My page name|link title>` or `<:page:My page title>`
* `<:doc:My fancy document.pdf>`
* `<:image:My pretty image.jpeg>`, `<:image:My pretty image.jpeg|left>` (`left` classname),
  `<:image:My pretty image.jpeg|right>` (`right` classname), `<:image:My pretty image.jpeg|full>` (`full-name` classname),
  `<:image:My pretty image.jpeg|width=123>` (outputs a rendition with `width-123`, and class `left`)

⚠️ these types of tags are not reliable as titles can and will change. Support for  will be removed in the future.

### Usage

You can use it as a `StreamField` block:

```python
from wagtail.blocks import StreamBlock

from wagtailmarkdown.blocks import MarkdownBlock


class MyStreamBlock(StreamBlock):
    markdown = MarkdownBlock(icon="code")
    # ...
```

<img src="https://i.imgur.com/4NFcfHd.png" width="728px" alt="">

Or use as a page field:

```python
from wagtail.admin.panels import FieldPanel
from wagtail.models import Page

from wagtailmarkdown.fields import MarkdownField


class MyPage(Page):
    body = MarkdownField()

    content_panels = [
        FieldPanel("title", classname="full title"),
        FieldPanel("body"),
    ]
```

And render the content in a template:

```html+django
{% load wagtailmarkdown %}
<article>
{{ self.body|markdown }}
</article>
```

<img src="https://i.imgur.com/Sj1f4Jh.png" width="728px" alt="">


## Compatibility

wagtail-markdown supports Wagtail 5.2 and above, python-markdown 3.3 and above.

## Contributing

All contributions are welcome!

### Installation

To make changes to this project, first clone this repository:

```shell
git clone git@github.com:torchbox/wagtail-markdown.git
cd wagtail-markdown
```

With your preferred Python virtual environment activated, install testing dependencies:

```shell
pip install -e '.[testing]' -U
```

### pre-commit

Note that this project uses [pre-commit](https://github.com/pre-commit/pre-commit). To set up locally:

```shell
# if you don't have it yet
$ pip install pre-commit
# go to the project directory
$ cd wagtail-markdown
# initialize pre-commit
$ pre-commit install

# Optional, run all checks once for this, then the checks will run only on the changed files
$ pre-commit run --all-files
```

### How to run tests

To run all tests in all environments:

```sh
tox -p
```

To run tests for a specific environment:

```shell
tox -e py313-django5.1-wagtail6.3
```

or, a specific test

```shell
tox -e py313-django5.1-wagtail6.3 -- tests.testapp.tests.test_admin.TestFieldsAdmin
```
