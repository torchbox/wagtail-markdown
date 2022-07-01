## wagtail-markdown: Markdown fields and blocks for Wagtail

[![Build status](https://img.shields.io/github/workflow/status/torchbox/wagtail-markdown/CI/main?style=for-the-badge)](https://github.com/torchbox/wagtail-markdown/actions)
[![PyPI](https://img.shields.io/pypi/v/wagtail-markdown.svg?style=for-the-badge)](https://pypi.org/project/wagtail-markdown/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge)](https://github.com/pre-commit/pre-commit)


Tired of annoying rich text editors getting in the way of your content
input?  Wish Wagtail worked more like a wiki?  Well, now it can.

`wagtail-markdown` provides Markdown field support for [Wagtail](https://github.com/torchbox/wagtail/).
Specifically, it provides:

* A `wagtailmarkdown.blocks.MarkdownBlock` for use in StreamFields.
* A `wagtailmarkdown.fields.MarkdownField` for use in Page models.
* A `wagtailmarkdown.edit_handlers.MarkdownPanel` for use in the editor interface.
* A `markdown` template tag.

The markdown rendered is based on `python-markdown`, but with several
extensions to make it actually useful in Wagtail:

* Tables.
* [Code highlighting](#syntax-highlighting).
* Inline links to pages (`<:My page name|link title>`) and documents
  (`<:doc:My fancy document.pdf>`), and inline images
  (`<:image:My pretty image.jpeg>`).
* Inline Markdown preview using [EasyMDE](https://github.com/Ionaru/easy-markdown-editor)

These are implemented using the `python-markdown` extension interface.

### Installation
Available on PyPi - https://pypi.org/project/wagtail-markdown/.

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

All `wagtatail-markdown` settings are defined in a single `WAGTAILMARKDOWN` dictionary in your settings file:

```python
# settings.py

WAGTAILMARKDOWN = {
    "autodownload_fontawesome": False,
    "allowed_tags": [],  # optional. a list of HTML tags. e.g. ['div', 'p', 'a']
    "allowed_styles": [],  # optional. a list of styles
    "allowed_attributes": {},  # optional. a dict with HTML tag as key and a list of attributes as value
    "extensions": [],  # optional. a list of python-markdown supported extensions
    "extension_configs": {},  # optional. a dictionary with the extension name as key, and its configuration as value
}
```

Note: `allowed_tags`, `allowed_styles`, `allowed_attributes`, `extensions` and `extension_configs` are added to the
[default wagtail-markdown settings](https://github.com/torchbox/wagtail-markdown/blob/main/wagtailmarkdown/utils.py#L40).


#### Custom FontAwesome Configuration - `autodownload_fontawesome`
The EasyMDE editor is compatible with [FontAwesome 5](https://fontawesome.com/how-to-use/graphql-api/intro/getting-started).
By default EasyMDE will get version 4.7.0 from a CDN. To specify your own version, set

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
from wagtail.core import hooks
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
from wagtail.core import hooks
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


### Usage

You can use it as a `StreamField` block:

```python
from wagtail.core.blocks import StreamBlock

from wagtailmarkdown.blocks import MarkdownBlock


class MyStreamBlock(StreamBlock):
    markdown = MarkdownBlock(icon="code")
    # ...
```

<img src="https://i.imgur.com/4NFcfHd.png" width="728px" alt="">

Or use as a page field:

```python
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.models import Page

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

wagtail-markdown supports Wagtail 2.15 and above.

## Contributing

All contributions are welcome!

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

Now you can run tests as shown below:

```sh
tox -p
```

or, you can run them for a specific environment `tox -e py39-django3.2-wagtail2.15` or specific test
`tox -e py39-django3.2-wagtail2.15 tests.testapp.tests.test_admin.TestFieldsAdmin`
