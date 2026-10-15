import re

from django.core.cache import cache
from django.test import TestCase, override_settings
from wagtail.images.tests.utils import Image, get_test_image_file

from wagtailmarkdown.mdx.inlinepatterns import ImageExtension
from wagtailmarkdown.templatetags.wagtailmarkdown import markdown


@override_settings(
    WAGTAILMARKDOWN={"image_template": "wagtailmarkdown/responsive_image.html"}
)
class TestImageTemplate(TestCase):
    def setUp(self):
        self.image = Image.objects.create(
            title="Test image",
            file=get_test_image_file(size=(1, 1)),
        )
        self.addCleanup(
            lambda: [
                rendition.file.delete(save=False)
                for rendition in self.image.renditions.all()
            ]
        )
        self.addCleanup(lambda: self.image.file.delete(save=False))

    def test_image_alone_in_paragraph_is_a_figure_with_picture(self):
        html = markdown(f"Before\n\n![alt text](image:{self.image.pk})\n\nAfter")

        self.assertTrue(html.startswith('<p>Before</p>\n<figure class="left">'))
        self.assertTrue(html.endswith("</figure>\n<p>After</p>"))
        self.assertIn("<picture>", html)
        self.assertRegex(
            html, r'<source sizes="100vw" srcset="[^"]*width-400\.format-webp'
        )
        self.assertIn('type="image/webp"', html)
        self.assertRegex(html, r'<img alt="alt text"[^>]* loading="lazy"')
        for width in (400, 800, 1200, 1600):
            self.assertIn(f"width-{width}.format-jpeg", html)
        self.assertNotIn("figcaption", html)

    def test_title_becomes_the_caption(self):
        html = markdown(
            f'![alt text](image:{self.image.pk},class=right "A <b>caption</b>")'
        )

        self.assertTrue(html.startswith('<figure class="right"><picture>'))
        self.assertIn("<figcaption>A &lt;b&gt;caption&lt;/b&gt;</figcaption>", html)
        self.assertRegex(html, r'<img alt="alt text"')
        self.assertNotIn("title=", html)

    def test_image_inside_text_is_a_picture_in_the_paragraph(self):
        html = markdown(
            f'Look ![alt text](image:{self.image.pk},class=right "Tip") here.'
        )

        self.assertTrue(html.startswith("<p>Look <picture>"))
        self.assertTrue(html.endswith("</picture> here.</p>"))
        self.assertNotIn("<figure", html)
        self.assertRegex(html, r'<img alt="alt text" class="right"[^>]* title="Tip"')

    def test_filter_serves_exactly_that_rendition(self):
        rendition = self.image.get_rendition("width-40")

        standalone = markdown(f"![alt text](image:{self.image.pk},filter=width-40)")
        inline = markdown(f"An ![icon](image:{self.image.pk},filter=width-40) here")

        self.assertEqual(
            standalone,
            f'<figure class="left"><img src="{rendition.url}" width="1" height="1" '
            'alt="alt text" loading="lazy"></figure>',
        )
        self.assertEqual(
            inline,
            f'<p>An <img src="{rendition.url}" width="1" height="1" alt="icon" '
            'class="left" loading="lazy"> here</p>',
        )
        self.assertNotIn("<picture>", standalone + inline)

    def test_invalid_filter_falls_back_to_the_picture(self):
        html = markdown(f"![alt text](image:{self.image.pk},filter=nope)")

        self.assertIn("<picture>", html)

    def test_escaped_and_empty_alt_text(self):
        escaped = markdown(f"![A \\[red\\] cliff](image:{self.image.pk})")
        decorative = markdown(f"![](image:{self.image.pk})")

        self.assertRegex(escaped, r'<img alt="A \[red\] cliff"')
        self.assertRegex(decorative, r'<img alt=""')

    def test_same_image_twice_keeps_each_alt_text(self):
        html = markdown(
            f"![First](image:{self.image.pk})\n\n"
            f"Inline ![Second](image:{self.image.pk}) and "
            f"![Third](image:{self.image.pk},class=right)."
        )

        self.assertEqual(
            re.findall(r'<img alt="([^"]*)"', html), ["First", "Second", "Third"]
        )

    def test_missing_image_is_unchanged(self):
        self.assertEqual(
            markdown("![image not found](image:12345)"),
            '<p><img alt="image not found" src="image:12345"></p>',
        )

    def test_placeholder_looking_text_stays_text(self):
        html = markdown("WAGTAILMARKDOWNIMAGE0123456789abcdefN0")

        self.assertEqual(html, "<p>WAGTAILMARKDOWNIMAGE0123456789abcdefN0</p>")

    def test_markdown_inside_code_is_not_an_image(self):
        html = markdown(f"`![alt](image:{self.image.pk})`")

        self.assertEqual(html, f"<p><code>![alt](image:{self.image.pk})</code></p>")

    @override_settings(
        WAGTAILMARKDOWN={
            "image_template": "wagtailmarkdown/responsive_image.html",
            "extensions": ["toc"],
        }
    )
    def test_image_in_heading_is_left_out_of_the_heading_id(self):
        html = markdown(f"# Head ![alt text](image:{self.image.pk})")

        self.assertTrue(html.startswith('<h1 id="head">Head <picture>'))
        self.assertNotIn("wagtailmarkdownimage", html.lower())

    def test_missing_image_file_with_filter_renders_a_broken_image(self):
        # Image ids are reused between tests, so drop renditions cached by others.
        cache.clear()
        self.image.file.delete(save=False)

        html = markdown(f"![alt text](image:{self.image.pk},filter=width-40)")

        self.assertEqual(
            html,
            '<figure class="left"><img src="/not-found" width="0" height="0" '
            'alt="alt text" loading="lazy"></figure>',
        )

    @override_settings(
        WAGTAILMARKDOWN={
            "extensions": [ImageExtension(template_name="testapp/markdown_image.html")],
            "extensions_settings_mode": "override",
        }
    )
    def test_template_name_given_to_the_extension(self):
        html = markdown(f"![A cliff](image:{self.image.pk})")

        self.assertIn('data-alt="A cliff"', html)

    @override_settings(
        WAGTAILMARKDOWN={"image_template": "testapp/markdown_image.html"}
    )
    def test_custom_template_gets_the_context(self):
        rendition = self.image.get_rendition("width-40")

        html = markdown(
            f'![A cliff](image:{self.image.pk},class=right,filter=width-40 "Sunset")'
        )

        self.assertEqual(
            html,
            f'<span data-standalone="True" data-class="right" data-alt="A cliff" '
            f'data-caption="Sunset" data-image="{self.image.pk}" '
            f'data-rendition="{rendition.url}"></span>',
        )


class TestWithoutImageTemplate(TestCase):
    def test_default_output_is_unchanged(self):
        image = Image.objects.create(
            title="Test image", file=get_test_image_file(size=(1, 1))
        )
        self.addCleanup(lambda: image.file.delete(save=False))
        self.addCleanup(
            lambda: [
                rendition.file.delete(save=False)
                for rendition in image.renditions.all()
            ]
        )

        self.assertEqual(
            markdown(f'![alt text](image:{image.pk} "Title")'),
            f'<p><img alt="alt text" class="left" '
            f'src="{image.get_rendition("width-500").url}" title="Title"></p>',
        )
