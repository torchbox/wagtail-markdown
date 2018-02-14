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
* Code highlighting.
* Inline links to pages (`<:My page name|link title>`) and documents
  (`<:doc:My fancy document.pdf>`), and inline images
  (`<:image:My pretty image.jpeg>`).
* Inline Markdown preview using [SimpleMDE](http://nextstepwebs.github.io/simplemde-markdown-editor/)

These are implemented using the `python-markdown` extension interface.
Currently, adding new extensions isn't possible without modifying the code, but
that shouldn't be difficult to implement (patches welcome).

### Installation
Alpha release is available on Pypi - https://pypi.org/project/wagtail-markdown/ - installable via `pip install wagtail-markdown`. It's not a production ready release.


### Using it

Add it to `INSTALLED_APPS`:

```
INSTALLED_APPS = (
...
    'wagtailmarkdown',
...
)
```

Use it as a `StreamField` block:

```
from wagtailmarkdown.blocks import MarkdownBlock

class MyStreamBlock(StreamBlock):
    markdown = MarkdownBlock(icon="code")
```

<img src="https://i.imgur.com/4NFcfHd.png" width="728px" alt="">

Or use as a page field:

```
from wagtailmarkdown.edit_handlers import MarkdownPanel
from wagtailmarkdown.fields import MarkdownField

class MyPage(Page):
    body = models.MarkdownField()

    content_panels = [
        FieldPanel("title", classname="full title"),
        MarkdownPanel("body"),
    ]
```

And render the content in a template:

```
{% load wagtailmarkdown %}
<article>
{{ self.body|markdown }}
</article>
```

<img src="https://i.imgur.com/Sj1f4Jh.png" width="728px" alt="">

To enable syntax highlighting please use the Pygments (`pip install Pygments`) library.

NB: The current version was written in about an hour and is probably completely
unsuitable for production use.  Testing, comments and feedback are welcome:
<tomasz.knapik@torchbox.com> (or open a Github issue).

### TODO

* Make a alpha/beta release and submit to PyPI
* Set up CI
* Set up tests
