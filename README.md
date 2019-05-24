## wagtail-markdown: Markdown fields and blocks for Wagtail

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
* Inline Markdown preview using [SimpleMDE](http://nextstepwebs.github.io/simplemde-markdown-editor/)

These are implemented using the `python-markdown` extension interface.
Currently, adding new extensions isn't possible without modifying the code, but
that shouldn't be difficult to implement (patches welcome).

### Installation
Alpha release is available on Pypi - https://pypi.org/project/wagtail-markdown/ - installable via `pip install wagtail-markdown`. It's not a production ready release.

The SimpleMDE editor uses FontAwesome for its widget icons. You can install [Wagtail FontAwesome](https://gitlab.com/alexgleason/wagtailfontawesome) via `pip install wagtailfontawesome`, or if you already have the stylesheet,  add the following to a `wagtail_hooks` module in a registered app in your project:

``` python
@hooks.register('insert_global_admin_css')
def import_fontawesome_stylesheet():
    elem = '<link rel="stylesheet" href="{}path/to/font-awesome.min.css">'.format(
        settings.STATIC_URL
    )
    return format_html(elem)
```

#### Syntax highlighting

Syntax highlighting using codehilite is an optional feature, which works by
adding CSS classes to the generated HTML. To use these classes, you will need
to install Pygments (`pip install Pygments`), and to generate an appropriate
stylesheet. You can generate one as per the [Pygments
documentation](http://pygments.org/docs/quickstart/), with:

``` python
>>> from pygments.formatters import HtmlFormatter
>>> print HtmlFormatter().get_style_defs('.codehilite')
```

Save the output to a file and reference it somewhere that will be
picked up on pages rendering the relevant output, e.g. your base template:

``` html+django
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
