## wagtail-markdown: Markdown fields and blocks for Wagtail

Tired of annoying rich text editors getting in the way of your content
input?  Wish Wagtail worked more like a wiki?  Well, now it can.

`wagtail-markdown` provides Markdown field support for [Wagtail](https://github.com/torchbox/wagtail/).
Specifically, it provides:

* A `MarkdownBlock` for use in streamfields.
* A MarkdownPanel and MarkdownPanel for use in the editor interface.
* A Markdown template tag.

The markdown rendered is based on `python-markdown`, but with several
extensions to make it actually useful in Wagtail:

* Tables.
* Code highlighting.
* Inline links to pages (`<:My page name|link title>`), images
  (`<:image:My pretty image.jpeg>`), documents, etc.
* Inline Markdown preview using [SimpleMDE](http://nextstepwebs.github.io/simplemde-markdown-editor/)

### Using it

Use it as a `StreamField` block:

```
from wagtailmarkdown import MarkdownBlock

class MyStreamBlock(StreamBlock):
    markdown = MarkdownBlock(icon="code")
```

Or use as a page field:

```
from wagtailmarkdown import MarkdownField, MarkdownPanel

class MyPage(Page):
    body = models.MarkdownField()

MyPage.content_panels = [
    FieldPanel("title", classname="full title"),
    MarkdownPanel("body"),
]
```

And render the content in a template:

```
<article>
{{ self.body|markdown }}
</article>
```

NB: The current version was written in about an hour and is probably completely 
unsuitable for production use.  Testing, comments and feedback are welcome: 
<felicity@torchbox.com> (or open a Github issue).

### TODO

* Using the `markdown` filter in the template should not be necessary.
* SimpleMDE should work with Streamfield.
