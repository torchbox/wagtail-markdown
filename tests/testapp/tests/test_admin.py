from django.test import TestCase, override_settings
from django.urls import reverse

from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.core.models import Page
from wagtail.tests.utils import WagtailTestUtils

from wagtailmarkdown.blocks import MarkdownBlock
from wagtailmarkdown.fields import MarkdownField
from wagtailmarkdown.widgets import MarkdownTextarea


class TestFieldsAdmin(TestCase, WagtailTestUtils):
    def setUp(self):
        self.user = self.login()
        self.root_page = Page.objects.first()

    def test_markdown_field_in_admin(self):
        response = self.client.get(
            reverse(
                "wagtailadmin_pages:add",
                args=("testapp", "testpage", self.root_page.id),
            )
        )

        self.assertContains(response, '<script>easymdeAttach("id_body");</script>')
        self.assertContains(response, "easymde.attach.js")

    def test_markdown_block(self):
        block = MarkdownBlock()
        self.assertEqual(block.render_basic("# hello"), "<h1>hello</h1>")

    def test_markdown_block_in_admin(self):
        response = self.client.get(
            reverse(
                "wagtailadmin_pages:add",
                args=("testapp", "testwithstreamfieldpage", self.root_page.id),
            )
        )
        self.assertContains(response, "easymde.attach.js")
        if WAGTAIL_VERSION >= (2, 13):
            self.assertContains(
                response,
                "[&quot;markdown&quot;, {&quot;_type&quot;: "
                "&quot;wagtailmarkdown.widgets.MarkdownTextarea&quot;, "
                "&quot;_args&quot;: [&quot;&lt;textarea name=\\&quot;__NAME__\\"
                "&quot; cols=\\&quot;40\\&quot; "
                "rows=\\&quot;1\\&quot; id=\\&quot;__ID__\\&quot;&gt;\\n&lt;/textarea&gt;"
                "&lt;script&gt;easymdeAttach(\\&quot;__ID__\\&quot;);"
                "&lt;/script&gt;&quot;, &quot;__ID__&quot;]}",
            )
            self.assertContains(response, "markdown-textarea-adapter.js")
        else:
            self.assertContains(
                response,
                '<textarea name="__PREFIX__-value" cols="40" rows="1" '
                'id="__PREFIX__-value" placeholder="Markdown">\n</textarea>'
                '<script>easymdeAttach("__PREFIX__-value");<-/script>',
            )

    def test_markdown_field(self):
        field = MarkdownField()
        self.assertEqual(type(field.formfield().widget), MarkdownTextarea)

    def test_widget(self):
        widget = MarkdownTextarea()
        init = widget.render_js_init("the_id", "name", "value")

        self.assertEqual(init, 'easymdeAttach("the_id");')

        with override_settings(WAGTAILMARKDOWN={"autodownload_fontawesome": False}):
            init = widget.render_js_init("the_id", "name", "value")
            self.assertEqual(init, 'easymdeAttach("the_id", false);')
