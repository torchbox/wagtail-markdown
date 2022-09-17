from django.test import TestCase

from wagtail.documents import get_document_model
from wagtail.documents.tests.utils import get_test_document_file
from wagtail.images.tests.utils import Image, get_test_image_file

from testapp.models import TestPage

from wagtailmarkdown.templatetags.wagtailmarkdown import markdown


try:
    from wagtail.models import Page
except ImportError:
    from wagtail.core.models import Page


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

table_input = """
First Header   | Second Header
-------------- | -------------
Content Cell 1 | Content Cell 2
Content Cell 3 | Content Cell 4
"""

table_output = (
    "<table><thead><tr><th>First Header</th><th>Second Header</th></tr></thead>"
    "<tbody><tr><td>Content Cell 1</td><td>Content Cell 2</td></tr>"
    "<tr><td>Content Cell 3</td><td>Content Cell 4</td></tr></tbody></table>"
)


class TestTemplateTags(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root_page = Page.objects.get(id=2)

        page1 = TestPage(title="test", slug="test1")
        cls.root_page.add_child(instance=page1)

        page2 = TestPage(title="test", slug="test2")
        cls.root_page.add_child(instance=page2)

        page3 = TestPage(title="test3", slug="test3")
        cls.root_page.add_child(instance=page3)

    def setUp(self):
        self.image = Image.objects.create(
            title="test_image.png",
            file=get_test_image_file(size=(1, 1)),
        )
        self.document = get_document_model().objects.create(
            title="Test document", file=get_test_document_file()
        )

    def tearDown(self):
        for rendition in self.image.renditions.all():
            rendition.file.delete(False)
        self.image.file.delete(False)
        self.document.file.delete(False)

    def test_markdown_transformed_to_html(self):
        self.assertEqual(markdown("# heading"), "<h1>heading</h1>")
        self.assertEqual(markdown("**strong**"), "<p><strong>strong</strong></p>")

    def test_transformed_html_sanitised(self):
        self.assertEqual(markdown(markdown_input), expected_output)

    def test_markdown_table(self):
        self.assertEqual(markdown(table_input).replace("\n", ""), table_output)

    def test_markdown_linker_page_404(self):
        self.assertEqual(
            markdown("<:page:not-found>"), '<p>[page "not-found" not found]</p>'
        )

    def test_markdown_linker_page_multiple(self):
        self.assertEqual(
            markdown("<:page:test>"), '<p>[multiple pages "test" found]</p>'
        )

    def test_markdown_linker_page_simple(self):
        self.assertEqual(
            markdown("<:page:test3>"), '<p><a href="/test3/">test3</a></p>'
        )

    def test_markdown_linker_wrong_type(self):
        self.assertEquals(
            markdown("<:foobar:test3>"), '<p>[invalid linker type "foobar"]</p>'
        )

    def test_markdown_linker_image_not_found(self):
        self.assertEquals(markdown("<:image:nope>"), '<p>[image "nope" not found]</p>')

    def test_markdown_linker_image(self):
        self.assertEqual(
            markdown("<:image:test_image.png>"),
            '<p><a href="/original_images/test.png">'
            '<img class="left" src="/images/test.width-500.png"></a></p>',
        )

    def test_markdown_linker_doc(self):
        self.assertEqual(
            markdown("<:doc:Test document>"),
            '<p><a href="/documents/test.txt">Test document</a></p>',
        )
