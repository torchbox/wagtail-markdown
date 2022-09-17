from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from wagtailmarkdown.blocks import MarkdownBlock
from wagtailmarkdown.fields import MarkdownField


class TestPage(Page):
    body = MarkdownField(blank=True)
    content_panels = Page.content_panels + [FieldPanel("body")]


class MyStreamBlock(StreamBlock):
    markdown = MarkdownBlock(icon="code")


class TestWithStreamFieldPage(Page):
    body = StreamField(MyStreamBlock, blank=True)
    content_panels = Page.content_panels + [
        FieldPanel("body") if WAGTAIL_VERSION >= (3, 0) else StreamFieldPanel("body")
    ]
