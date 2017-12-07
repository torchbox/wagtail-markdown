## wagtail-markdown: Markdown fields and blocks for Wagtail

Tired of annoying rich text editors getting in the way of your content
input?  Wish Wagtail worked more like a wiki?  Well, now it can.

`wagtail-markdown` provides Markdown field support for [Wagtail](https://github.com/torchbox/wagtail/).
Specifically, it provides:

* A `MarkdownBlock` for use in streamfields.
* A `MarkdownField` for use in page models.
* A `MarkdownPanel` for use in the editor interface.
* A `markdown` template tag.

The markdown rendered is based on `python-markdown`, but with several
extensions to make it actually useful in Wagtail:

* Tables.
* Code highlighting.
* Inline links to pages (`<:My page name|link title>`) and documents
  (`<:doc:My fancy document.pdf>`), and inline images
  (`<:image:My pretty image.jpeg>`).
* Inline Markdown preview using [SimpleMDE](http://nextstepwebs.github.io/simplemde-markdown-editor/)

These are implemented using the `python-markdown` extension interface.
Currently, adding new extensions isn't possible without modifying the code, but
that shouldn't be difficult to implement (patches welcome).


#### Compatibility

`wagtail-markdown` is compatible with Wagtail 1.4 and above.


### Installation

Add it to `INSTALLED_APPS`:

``` python
INSTALLED_APPS = (
...
    'wagtailmarkdown',
...
)
```

The SimpleMDE editor uses FontAwesome for its widget icons. You need to add the
following to a `wagtail_hooks` module in a registered app in your project:

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
stylesheet. You can generate one as per the [pygments
documentation](http://pygments.org/docs/quickstart/), with:

``` python
>>> from pygments.formatters import HtmlFormatter
>>> print HtmlFormatter().get_style_defs('.codehilite')
```

And then saving the output to a file and referencing it somewhere that will be
picked up on pages rendering the relevant output, e.g. your base template:

``` htmldjango
        <link rel="stylesheet" type="text/css" href="{% static 'path/to/pygments.css' %}">
```


### Using it

Use it as a `StreamField` block:

``` python
from wagtailmarkdown.fields import MarkdownBlock

class MyStreamBlock(StreamBlock):
    markdown = MarkdownBlock(icon="code")
```

<img src="https://i.imgur.com/4NFcfHd.png" width="728px" alt="">

Or use as a page field:

``` python
from wagtailmarkdown.fields import MarkdownField, MarkdownPanel

class MyPage(Page):
    body = models.MarkdownField()

MyPage.content_panels = [
    FieldPanel("title", classname="full title"),
    MarkdownPanel("body"),
]
```

And render the content in a template:

``` htmldjango
{% load wagtailmarkdown %}
<article>
{{ self.body|markdown }}
</article>
```

<img src="https://i.imgur.com/Sj1f4Jh.png" width="728px" alt="">

NB: The current version was written in about an hour and is probably completely
unsuitable for production use.  Testing, comments and feedback are welcome:
<felicity@torchbox.com> (or open a Github issue).

### TODO

* Using the `markdown` filter in the template should not be necessary.
