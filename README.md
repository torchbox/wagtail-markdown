## wagtail-markdown: Markdown fields and blocks for Wagtail

Tired of annoying rich text editors getting in the way of your content
input?  Wish Wagtail worked more like a wiki?  Well, now it can.

`wagtail-markdown` provides Markdown field support for Wagtail.
Specifically, it provides:

* A `MarkdownField` for use in page models (not yet implemented!)
* A `MarkdownBlock` for use in streamfields

The markdown rendered is based on `python-markdown`, but with several
extensions to make it actually useful in Wagtail:

* Tables.
* Code highlighting.
* Inline links to pages (`<:My page name|link title>`), images
  (`<:image:My pretty image.jpeg>`), documents, etc.

NB: The current version was written in about an hour and is probably completely 
unsuitable for production use.  Testing, comments and feedback are welcome: 
<felicity@torchbox.com> (or open a Github issue).
