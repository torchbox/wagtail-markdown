## wagtail-markdown: Markdown fields and blocks for Wagtail

[![Build status](https://img.shields.io/github/workflow/status/torchbox/wagtail-markdown/CI/main?style=for-the-badge)](https://github.com/torchbox/wagtail-markdown/actions)
[![PyPI](https://img.shields.io/pypi/v/wagtail-markdown.svg?style=for-the-badge)](https://pypi.org/project/wagtail-markdown/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white&style=for-the-badge)](https://github.com/pre-commit/pre-commit)


Tired of annoying rich text editors getting in the way of your content
input?  Wish Wagtail worked more like a wiki?  Well, now it can.

`wagtail-markdown` provides Markdown field support for [Wagtail](https://github.com/torchbox/wagtail/).
Specifically, it provides:

* A `wagtailmarkdown.blocks.MarkdownBlock` for use in streamfields.
* A `wagtailmarkdown.fields.MarkdownField` for use in page models.
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

You can configure wagtail-markdown to use additional Markdown extensions using the `WAGTAILMARKDOWN_EXTENSIONS` setting.

For example, to enable the [Table of
Contents](https://python-markdown.github.io/extensions/toc/) and [Sane
Lists](https://python-markdown.github.io/extensions/sane_lists/) extensions:
```python
WAGTAILMARKDOWN_EXTENSIONS = ["toc", "sane_lists"]
```

Extensions can be configured too:

```python
WAGTAILMARKDOWN_EXTENSIONs_CONFIG = {'pymdownx.arithmatex': {'generic': True}}
```

### Installation
Available on PyPi - https://pypi.org/project/wagtail-markdown/ - installable via `pip install wagtail-markdown`.

The EasyMDE editor is compatible with [FontAwesome 5](https://fontawesome.com/how-to-use/graphql-api/intro/getting-started).
By default EasyMDE will get version 4.7.0 from a CDN. To specify your own version, set
`WAGTAILMARKDOWN_AUTODOWNLOAD_FONTAWESOME = False` in your settings.

Then get the desired FontAwesome version. For the latest version you can use:

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

@hooks.register('insert_global_admin_css')
def import_fontawesome_stylesheet():
    elem = '<link rel="stylesheet" href="{}path/to/font-awesome.min.css">'.format(
        settings.STATIC_URL
    )
    return format_html(elem)
```

Note that due to the way EasyMDE defines the toolbar icons it is not compatible with [Wagtail FontAwesome](https://gitlab.com/alexgleason/wagtailfontawesome)

#### Syntax highlighting

Syntax highlighting using codehilite is an optional feature, which works by
adding CSS classes to the generated HTML. To use these classes, you will need
to install Pygments (`pip install Pygments`), and to generate an appropriate
stylesheet. You can generate one as per the [Pygments documentation](http://pygments.org/docs/quickstart/), with:

```python
>>> from pygments.formatters import HtmlFormatter
>>> print HtmlFormatter().get_style_defs('.codehilite')
```

Save the output to a file and reference it somewhere that will be
picked up on pages rendering the relevant output, e.g. your base template:

```html+django
<link rel="stylesheet" type="text/css" href="{% static 'path/to/pygments.css' %}">
```


### Using it

Add it to `INSTALLED_APPS`:

```python
INSTALLED_APPS += [
    'wagtailmarkdown',
]
```

Use it as a `StreamField` block:

```python
from wagtailmarkdown.blocks import MarkdownBlock

class MyStreamBlock(StreamBlock):
    markdown = MarkdownBlock(icon="code")
```

<img src="https://i.imgur.com/4NFcfHd.png" width="728px" alt="">

Or use as a page field:

```python
from wagtailmarkdown.edit_handlers import MarkdownPanel
from wagtailmarkdown.fields import MarkdownField

class MyPage(Page):
    body = MarkdownField()

    content_panels = [
        FieldPanel("title", classname="full title"),
        MarkdownPanel("body"),
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

To enable syntax highlighting please use the Pygments (`pip install Pygments`) library.

NB: The current version was written in about an hour and is probably completely
unsuitable for production use.  Testing, comments and feedback are welcome:
<kevin.howbrook@torchbox.com> (or open a Github issue).


### Roadmap for 0.5

* Set up tests: https://github.com/torchbox/wagtail-markdown/issues/28
