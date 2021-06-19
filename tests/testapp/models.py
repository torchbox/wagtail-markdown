from wagtail.admin.edit_handlers import StreamFieldPanel
from wagtail.core.blocks import StreamBlock
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from wagtailmarkdown.blocks import MarkdownBlock
from wagtailmarkdown.edit_handlers import MarkdownPanel
from wagtailmarkdown.fields import MarkdownField


class TestPage(Page):
    body = MarkdownField(blank=True)
    content_panels = [MarkdownPanel("body")]


class MyStreamBlock(StreamBlock):
    markdown = MarkdownBlock(icon="code")


class TestWithStreamFieldPage(Page):
    body = StreamField(MyStreamBlock, blank=True)
    content_panels = [StreamFieldPanel("body")]
