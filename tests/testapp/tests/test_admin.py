from django.test import TestCase, override_settings
from django.urls import reverse
from wagtail import VERSION as WAGTAIL_VERSION
from wagtail.models import Page
from wagtail.test.utils import WagtailTestUtils

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
        self.assertContains(response, "easymde.attach.js")

        if WAGTAIL_VERSION >= (6, 0):
            self.assertContains(
                response,
                '<textarea name="body" cols="40" rows="10" id="id_body" data-controller="easymde">',
            )
        else:
            self.assertContains(response, '<script>easymdeAttach("id_body");</script>')

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
        if WAGTAIL_VERSION < (6, 0):
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

    def test_markdown_field(self):
        field = MarkdownField()
        self.assertEqual(type(field.formfield().widget), MarkdownTextarea)

    def test_widget(self):
        widget = MarkdownTextarea()

        if WAGTAIL_VERSION >= (6, 0):
            init = widget.render("name", "value", attrs={"id": "the_id"})

            self.assertEqual(
                init,
                '<textarea name="name" cols="40" rows="10" id="the_id" data-controller="easymde">\nvalue</textarea>',
            )

            with override_settings(WAGTAILMARKDOWN={"autodownload_fontawesome": False}):
                init = widget.render("name", "value", attrs={"id": "the_id"})
                self.assertEqual(
                    init,
                    '<textarea name="name" cols="40" rows="10" id="the_id" data-controller="easymde" data-easymde-autodownload-value="false">\nvalue</textarea>',
                )
        else:
            init = widget.render_js_init("the_id", "name", "value")

            self.assertEqual(init, 'easymdeAttach("the_id");')

            with override_settings(WAGTAILMARKDOWN={"autodownload_fontawesome": False}):
                init = widget.render_js_init("the_id", "name", "value")
                self.assertEqual(init, 'easymdeAttach("the_id", false);')
