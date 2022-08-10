from io import BytesIO, StringIO

from django.test import TestCase
from django.core.files import File
from wagtail.core.models import Site
from wagtail.images.models import Image
from wagtail.documents.models import Document
from PIL import Image as PIL_Image
from testapp.models import TestPage

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

table_input = """
First Header   | Second Header
-------------- | -------------
Content Cell 1 | Content Cell 2
Content Cell 3 | Content Cell 4
"""

table_output = ("<table class=\"wftable\">"
    "<thead><tr><th>First Header</th><th>Second Header</th></tr></thead>"
    "<tbody><tr><td>Content Cell 1</td><td>Content Cell 2</td></tr>"
    "<tr><td>Content Cell 3</td><td>Content Cell 4</td></tr></tbody></table>"
)


class TestTemplateTags(TestCase):

    def setUp(self):
        self.p1 = TestPage(title="test", slug="test1", path="test1", depth=1)
        self.p1.save()
        self.p2 = TestPage(title="test", slug="test2", path="test2", depth=1)
        self.p2.save()
        self.p3 = TestPage(title="test3", slug="test3", path="test3", depth=1)
        self.p3.save()
        self.root = TestPage(title="root", path="root", depth=0)
        self.root.save()
        image = PIL_Image.new(mode="RGB", size=(100, 100))
        img_content = BytesIO()
        image.save(img_content, format="PNG")
        self.img = Image(title="test_image.png")
        self.img.file.save("test_image.png", File(img_content))
        self.img.save()
        self.doc = Document(title="test document")
        doc_content = StringIO()
        doc_content.write("foo bar")
        self.doc.file.save("test_doc.txt", File(doc_content))
        self.doc.save()
        self.site = Site.objects.first()
        self.site.root_page = self.root
        self.site.save()

    def test_markdown_transformed_to_html(self):
        self.assertEqual(markdown("# heading"), "<h1>heading</h1>")
        self.assertEqual(markdown("**strong**"), "<p><strong>strong</strong></p>")

    def test_transformed_html_sanitised(self):
        self.assertEqual(markdown(markdown_input), expected_output)

    def test_markdown_table(self):
        self.assertEqual(markdown(table_input).replace("\n", ""), table_output)

    def test_markdown_linker_404(self):
        self.assertEquals(markdown("<:page:not-found>"),
                          "<p>[page \"not-found\" not found]</p>")

    def test_markdown_linker_multiple(self):
        self.assertEquals(markdown("<:page:test>"),
                          "<p>[multiple pages \"test\" found]</p>")

    def test_markdown_linker_simple(self):
        self.assertEqual(markdown("<:page:test3>"), "<p><a href=\"/\">test3</a></p>")

    def test_markdown_linker_wrong_type(self):
        self.assertEquals(markdown("<:image:test3>"),
                          "<p>[image \"test3\" not found]</p>")

    def test_markdown_linker_image_not_found(self):
        self.assertEquals(markdown("<:image:nope>"),
                          "<p>[image \"nope\" not found]</p>")

    def test_markdown_linker_image(self):
        self.assertRegex(
            markdown("<:image:test_image.png>"),
            r'<p><a href="/original_images/test_image_[a-zA-Z0-9]{7}\.png"><img class='
            r'"left" src="/images/test_image_[a-zA-Z0-9]{7}\.width-500\.png"></a></p>')

    def test_markdown_linker_doc(self):
        self.assertRegex(
            markdown("<:doc:test document>"),
            r'<p><a href="/documents/test_doc_[a-zA-Z0-9]{7}\.txt">test document</a></p>')
