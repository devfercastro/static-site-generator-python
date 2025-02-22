import unittest

from src.markdown.extractor import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images_unique_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
        ]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_images_multiple_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        result = extract_markdown_images(text)
        self.assertEqual(result, expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links_unique(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
        ]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)

    def test_extract_markdown_links_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]
        result = extract_markdown_links(text)
        self.assertEqual(result, expected)


class TestExtractTitle(unittest.TestCase):
    def test_extract_title_base(self):
        h1 = "This is the header that I'm looking for"
        markdown = f"# {h1}\n\na paragraph\n\nanother paragraph"
        expected = h1
        result = extract_title(markdown)
        self.assertEqual(result, expected)

    def test_extract_title_invalid(self):
        with self.assertRaises(ValueError) as context:
            extract_title("markdown with no header")
        self.assertEqual(
            str(context.exception), "H1 header not encountered in markdown passed"
        )
