## wagtail-markdown: Markdown fields and blocks for Wagtail

Tired of annoying rich text editors getting in the way of your content
input?  Wish Wagtail worked more like a wiki?  Well, now it can.

`wagtail-markdown` provides Markdown field support for Wagtail.
Specifically, it provides:

* A `MarkdownBlock` for use in streamfields
* A Markdown template tag.

The markdown rendered is based on `python-markdown`, but with several
extensions to make it actually useful in Wagtail:

* Tables.
* Code highlighting.
* Inline links to pages (`<:My page name|link title>`), images
  (`<:image:My pretty image.jpeg>`), documents, etc.

Use as a `StreamField` block:

```
from wagtailmarkdown import MarkdownBlock

class MyStreamBlock(StreamBlock):
    markdown = MarkdownBlock(icon="code")
```

Use as a page field:

```
class MyPage(Page):
    body = models.TextField()
    subpage_types = []
    parent_page_types = ["home.SectionIndexPage"]

    search_fields = Page.search_fields + (
        SearchField("body"),
    )


MyPage.content_panels = [
    FieldPanel("title", classname="full title"),
    FieldPanel("body"),
]
```

And in a template:

```
<article>
{{ self.body|markdown }}
</article>
```

NB: The current version was written in about an hour and is probably completely 
unsuitable for production use.  Testing, comments and feedback are welcome: 
<felicity@torchbox.com> (or open a Github issue).
