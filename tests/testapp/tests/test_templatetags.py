from unittest import TestCase

from wagtailmarkdown.templatetags.wagtailmarkdown import markdown

markdown_input = (
    "# Heading\nThis is *some* text with a "
    "[link](https://example.com)\nand some disallowed "
    'tag and attributes: <i>italic</i>, <a data-attribute="foo">anchor tag</a> '
    "<script>alert('boom!')</script>"
)

expected_output = (
    "<h1>Heading</h1>\n<p>This is <em>some</em> "
    'text with a <a href="https://example.com">link</a>\n'
    "and some disallowed tag and attributes: &lt;i&gt;italic&lt;/i&gt;, "
    "<a>anchor tag</a> &lt;script&gt;alert('boom!')&lt;/script&gt;</p>"
)


class TestTemplateTags(TestCase):
    def test_markdown_transformed_to_html(self):
        self.assertEqual(markdown("# heading"), "<h1>heading</h1>")
        self.assertEqual(markdown("**strong**"), "<p><strong>strong</strong></p>")

    def test_transformed_html_sanitised(self):
        self.assertEqual(markdown(markdown_input), expected_output)
