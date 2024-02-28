from wagtail.admin.panels import FieldPanel
from wagtail.blocks import StreamBlock
from wagtail.fields import StreamField
from wagtail.models import Page

from wagtailmarkdown.blocks import MarkdownBlock
from wagtailmarkdown.fields import MarkdownField


class TestPage(Page):
    body = MarkdownField(blank=True)
    content_panels = Page.content_panels + [FieldPanel("body")]


class MyStreamBlock(StreamBlock):
    markdown = MarkdownBlock(icon="code")


class TestWithStreamFieldPage(Page):
    body = StreamField(
        MyStreamBlock,
        blank=True,
        use_json_field=True,
    )

    content_panels = Page.content_panels + [FieldPanel("body")]
