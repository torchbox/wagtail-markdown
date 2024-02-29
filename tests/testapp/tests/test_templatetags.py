from django.test import TestCase
from wagtail.documents import get_document_model
from wagtail.documents.tests.utils import get_test_document_file
from wagtail.images.tests.utils import Image, get_test_image_file
from wagtail.models import Page

from tests.testapp.models import TestPage
from wagtailmarkdown.mdx.inlinepatterns import _options_to_dict
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

table_output = (
    "<table><thead><tr><th>First Header</th><th>Second Header</th></tr></thead>"
    "<tbody><tr><td>Content Cell 1</td><td>Content Cell 2</td></tr>"
    "<tr><td>Content Cell 3</td><td>Content Cell 4</td></tr></tbody></table>"
)


class TestTemplateTags(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.root_page = Page.objects.get(id=2)

        cls.page1 = TestPage(title="test", slug="test1")
        cls.root_page.add_child(instance=cls.page1)

        page2 = TestPage(title="test", slug="test2")
        cls.root_page.add_child(instance=page2)

        page3 = TestPage(title="test3", slug="test3")
        cls.root_page.add_child(instance=page3)

    def setUp(self):
        self.image = Image.objects.create(
            title="Test image",
            file=get_test_image_file(size=(1, 1)),
        )
        self.document = get_document_model().objects.create(
            title="Test document", file=get_test_document_file()
        )

    def tearDown(self):
        for rendition in self.image.renditions.all():
            rendition.file.delete(save=False)
        self.image.file.delete(save=False)
        self.document.file.delete(save=False)

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

    def test_markdown_linker_page_with_title(self):
        self.assertEqual(
            markdown("<:page:test3|Link title>"),
            '<p><a href="/test3/">Link title</a></p>',
        )

    def test_markdown_linker_default(self):
        self.assertEqual(markdown("<:test3>"), '<p><a href="/test3/">test3</a></p>')

    def test_markdown_linker_wrong_type(self):
        self.assertEqual(
            markdown("<:foobar:test3>"), '<p>[invalid linker type "foobar"]</p>'
        )

    def test_markdown_linker_image(self):
        self.assertEqual(
            markdown("<:image:Test image>"),
            '<p><a href="/original_images/test.png">'
            '<img class="left" src="/images/test.width-500.png"></a></p>',
        )

    def test_markdown_linker_image_with_classname(self):
        self.assertEqual(
            markdown("<:image:Test image|left>"),
            '<p><a href="/original_images/test.png">'
            '<img class="left" src="/images/test.width-500.png"></a></p>',
        )
        self.assertEqual(
            markdown("<:image:Test image|right>"),
            '<p><a href="/original_images/test.png">'
            '<img class="right" src="/images/test.width-500.png"></a></p>',
        )
        self.assertEqual(
            markdown("<:image:Test image|full>"),
            '<p><a href="/original_images/test.png">'
            '<img class="full-width" src="/images/test.width-500.png"></a></p>',
        )

    def test_markdown_linker_image_with_rendition(self):
        self.assertEqual(
            markdown("<:image:Test image|width=200>"),
            '<p><a href="/original_images/test.png">'
            '<img class="left" src="/images/test.width-200.png"></a></p>',
        )
        self.assertEqual(
            markdown("<:image:Test image|width=foo>"),
            '<p><a href="/original_images/test.png">'
            '<img class="left" src="/images/test.width-500.png"></a></p>',
        )

    def test_markdown_linker_image_not_found(self):
        self.assertEqual(markdown("<:image:nope>"), '<p>[image "nope" not found]</p>')

    def test_markdown_linker_image_multiple(self):
        image = Image.objects.create(
            title="Test image",
            file=get_test_image_file(size=(1, 1)),
        )
        self.assertEqual(
            markdown("<:image:Test image>"),
            '<p>[multiple images "Test image" found]</p>',
        )

        image.file.delete(save=False)

    def test_markdown_linker_doc(self):
        self.assertEqual(
            markdown("<:doc:Test document>"),
            '<p><a href="/documents/test.txt">Test document</a></p>',
        )

    def test_markdown_linker_doc_with_title(self):
        self.assertEqual(
            markdown("<:doc:Test document|The document>"),
            '<p><a href="/documents/test.txt">The document</a></p>',
        )

    def test_markdown_linker_doc_not_found(self):
        self.assertEqual(
            markdown("<:doc:a document>"),
            '<p>[document "a document" not found]</p>',
        )

    def test_markdown_linker_doc_multiple(self):
        document = get_document_model().objects.create(
            title="Test document", file=get_test_document_file()
        )
        self.assertEqual(
            markdown("<:doc:Test document>"),
            '<p>[multiple documents "Test document" found]</p>',
        )

        document.file.delete(save=False)

    def test_markdown_inline_links(self):
        self.assertEqual(
            markdown(f"[Page link](page:{self.page1.pk})"),
            f'<p><a href="{self.page1.url}">Page link</a></p>',
        )
        self.assertEqual(
            markdown("[Non-existent page link](page:10000)"),
            '<p><a href="page:10000">Non-existent page link</a></p>',
        )

        self.assertEqual(
            markdown(f"[Document link](doc:{self.document.pk})"),
            f'<p><a href="{self.document.url}">Document link</a></p>',
        )
        self.assertEqual(
            markdown("[Non-existent document link](doc:12345)"),
            '<p><a href="doc:12345">Non-existent document link</a></p>',
        )

        self.assertEqual(
            markdown(f"![alt text](image:{self.image.pk})"),
            f'<p><img alt="alt text" class="left" '
            f'src="{self.image.get_rendition("width-500").url}"></p>',
        )
        self.assertEqual(
            markdown("![image not found](image:12345)"),
            '<p><img alt="image not found" src="image:12345"></p>',
        )

        self.assertEqual(
            markdown(f"![alt text](image:{self.image.pk}"),  # note: missing closing )
            "<p>![alt text](image:1</p>",
        )

    def test_markdown_inline_image_with_options(self):
        self.assertRegex(
            markdown(f"![alt text](image:{self.image.pk},class=left)"),
            r'<p><img alt="alt text" class="left" src="/images/test\.width-500\.png"></p>',
        )
        self.assertRegex(
            markdown(f"![alt text](image:{self.image.pk},class=right)"),
            r'<p><img alt="alt text" class="right" src="/images/test\.width-500\.png"></p>',
        )
        self.assertRegex(
            markdown(f"![alt text](image:{self.image.pk},classname=foo)"),
            r'<p><img alt="alt text" class="left" src="/images/test\.width-500\.png"></p>',
        )
        self.assertRegex(
            markdown(
                f"![alt text](image:{self.image.pk},filter=fill-200x200|format-jpeg)"
            ),
            r'<p><img alt="alt text" class="left" '
            r'src="/images/test[.a-z0-9]+\.fill-200x200\.format-jpeg\.jpg"></p>',
        )
        self.assertRegex(
            markdown(f"![alt text](image:{self.image.pk},filter=invalid-filter)"),
            r'<p><img alt="alt text" class="left" src="/images/test\.width-500\.png"></p>',
        )

    def test_markdown_options_to_dict(self):
        self.assertDictEqual(_options_to_dict(""), {})
        self.assertDictEqual(
            _options_to_dict("class=left"),
            {"class": "left"},
        )
        self.assertDictEqual(
            _options_to_dict("class=left, filter=fill-200x200"),
            {"class": "left", "filter": "fill-200x200"},
        )
        self.assertDictEqual(
            _options_to_dict("class=left,filter=fill-200x200|format-jpeg"),
            {"class": "left", "filter": "fill-200x200|format-jpeg"},
        )
        self.assertDictEqual(
            _options_to_dict("class=left,filter=fill-200x200, foo=bar ,"),
            {"class": "left", "filter": "fill-200x200", "foo": "bar"},
        )
        self.assertDictEqual(
            _options_to_dict("class=left,filter=fill-200x200, foo = bar ,baz"),
            {"class": "left", "filter": "fill-200x200", "foo": "bar"},
        )
        self.assertDictEqual(
            _options_to_dict("class=left,filter=fill-200x200,foo =bar,baz="),
            {"class": "left", "filter": "fill-200x200", "foo": "bar", "baz": ""},
        )
