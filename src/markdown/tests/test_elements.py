import unittest
import random
import re
from functools import reduce

from src.core import TextNode, TextType, HTMLNode
from src.markdown.elements import (
    parse_heading,
    parse_code,
    parse_quote,
    parse_unordered_list,
    parse_ordered_list,
    parse_paragraph,
)
from src.markdown.elements import extract_markdown_images, extract_markdown_links
from src.markdown.elements import split_nodes_link, split_nodes_image
from src.markdown.inline_parser import split_nodes_delimiter


class TestParseHeading(unittest.TestCase):
    def test_parse_heading_base(self):
        headers = [f"{"#" * i} heading {i}" for i in range(1, 7)]
        expected = [HTMLNode(f"h{i}", f"heading {i}") for i in range(1, 7)]
        result = [parse_heading(header) for header in headers]
        self.assertEqual(result, expected)

    def test_parse_heading_invalid(self):
        with self.assertRaises(ValueError) as context:
            parse_heading("####### heading 7 invalid")
        self.assertEqual(str(context.exception), "invalid markdown header syntax")
        with self.assertRaises(ValueError) as context:
            parse_heading("not valid")
        self.assertEqual(str(context.exception), "invalid markdown header syntax")


class TestParseCode(unittest.TestCase):
    def test_parse_code_base(self):
        code_block = "```\nfor i in range(0, 10):\n    print(i)```"
        code_content = code_block.strip("```\n")
        expected = HTMLNode("pre", None, [HTMLNode("code", code_content)])
        result = parse_code(code_block)
        self.assertEqual(result, expected)

    def test_parse_code_invalid(self):
        with self.assertRaises(ValueError) as context:
            parse_code("not valid code block")
        self.assertEqual(str(context.exception), "invalid markdown code block syntax")


class TestParseQuote(unittest.TestCase):
    def test_parse_quote_base(self):
        quote = "> this is a quote"
        quote_content = "this is a quote"
        expected = HTMLNode("blockquote", quote_content)
        result = parse_quote(quote)
        self.assertEqual(result, expected)


class TestParseUnorderedList(unittest.TestCase):
    def test_parse_unordered_list_base(self):
        list_items = [f"Item {i}" for i in range(1, 11)]

        unordered_list = reduce(
            lambda acc, list_item: acc + f"{random.choice(["-", "*"])} {list_item}\n",
            list_items,
            "",
        )
        expected = HTMLNode(
            "ul", None, [HTMLNode("li", list_item) for list_item in list_items]
        )
        result = parse_unordered_list(unordered_list)
        self.assertEqual(result, expected)


class TestParseOrderedList(unittest.TestCase):
    def test_parse_ordered_list(self):
        list_items = [f"Item {i}" for i in range(1, 11)]
        ordered_list = reduce(
            lambda acc, list_item: acc + f"{list_item[0] + 1}. {list_item[1]}\n",
            enumerate(list_items),
            "",
        )
        expected = HTMLNode(
            "ol", None, [HTMLNode("li", list_item) for list_item in list_items]
        )
        result = parse_ordered_list(ordered_list)
        self.assertEqual(result, expected)


class TestParseParagraph(unittest.TestCase):
    def test_parse_paragraph(self):
        paragraph = "this is some text"
        expected = HTMLNode("p", paragraph)
        result = parse_paragraph(paragraph)
        self.assertEqual(result, expected)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_basic(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("No delimiters here", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_multiple_delimiters(self):
        node = TextNode("**Hello** **world**", TextType.TEXT)
        expected = [
            TextNode("Hello", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("world", TextType.BOLD),
        ]
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, expected)

    def test_unmatched_delimiter_raises_error(self):
        node = TextNode("This is `code block", TextType.TEXT)
        delimiter = "`"
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], delimiter, TextType.CODE)
        self.assertEqual(str(context.exception), f'Unamtched delimiter "{delimiter}"')

    def test_mixed_nodes(self):
        node1 = TextNode("Some text with `code`", TextType.TEXT)
        node2 = TextNode("Bold text", TextType.BOLD)
        expected = [
            TextNode("Some text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            node2,
        ]
        result = split_nodes_delimiter([node1, node2], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_empty_parts(self):
        node = TextNode("``", TextType.TEXT)
        expected = [TextNode("", TextType.CODE)]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_leading_trailing_delimiters(self):
        node = TextNode("`code`", TextType.TEXT)
        expected = [TextNode("code", TextType.CODE)]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(result, [])

    def test_split_with_empty_strings(self):
        node = TextNode("Hello``world", TextType.TEXT)
        expected = [
            TextNode("Hello", TextType.TEXT),
            TextNode("", TextType.CODE),
            TextNode("world", TextType.TEXT),
        ]
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, expected)


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


class Image:
    def __init__(self, raw: str):
        self.raw = raw
        self.alt, self.url = re.findall(r"!\[(.*?)\]\((.*?)\)", raw)[0]


class TestSplitNodesImage(unittest.TestCase):
    image1 = Image("![rick roll](https://i.imgur.com/aKaOqIh.gif)")
    image2 = Image("![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
    image3 = Image("![example](https://example.com/image.png)")

    def test_split_nodes_image_no_image(self):
        """Test when there are no images in the text."""
        node = TextNode("This is plain text without any images.", TextType.TEXT)
        expected = [node]
        result = split_nodes_image([node])
        self.assertEqual(result, expected)

    def test_split_nodes_image_start_image(self):
        """Test when an image is at the start of the text."""
        trailing_text = " trailing text for test."
        node = TextNode(self.image1.raw + trailing_text, TextType.TEXT)
        expected = [
            TextNode(self.image1.alt, TextType.IMAGE, self.image1.url),
            TextNode(trailing_text, TextType.TEXT),
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected)

    def test_split_nodes_image_end_image(self):
        """Test when an image is at the end of the text."""
        leading_text = "leading text for test "
        node = TextNode(leading_text + self.image1.raw, TextType.TEXT)
        expected = [
            TextNode(leading_text, TextType.TEXT),
            TextNode(self.image1.alt, TextType.IMAGE, self.image1.url),
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected)

    def test_split_nodes_image_multiple_images(self):
        """Test when there are multiple images in the text."""
        node = TextNode(
            f"This is text with an image {
                self.image1.raw} and {self.image2.raw}",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode(self.image1.alt, TextType.IMAGE, self.image1.url),
            TextNode(" and ", TextType.TEXT),
            TextNode(self.image2.alt, TextType.IMAGE, self.image2.url),
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected)

    def test_split_nodes_image_mixed_nodes(self):
        """Test when there are mixed nodes (text, images, and other types)."""
        node1 = TextNode("This is plain text.", TextType.TEXT)
        node2 = TextNode(f"This has an {self.image1.raw}.", TextType.TEXT)
        node3 = TextNode("Another plain text.", TextType.TEXT)
        expected = [
            node1,
            TextNode("This has an ", TextType.TEXT),
            TextNode(self.image1.alt, TextType.IMAGE, self.image1.url),
            TextNode(".", TextType.TEXT),
            node3,
        ]
        result = split_nodes_image([node1, node2, node3])
        self.assertEqual(result, expected)

    def test_split_nodes_image_consecutive_images(self):
        """Test when there are consecutive images in the text."""
        node = TextNode(
            f"{self.image1.raw}{self.image2.raw}{
                self.image3.raw}",
            TextType.TEXT,
        )
        expected = [
            TextNode(self.image1.alt, TextType.IMAGE, self.image1.url),
            TextNode(self.image2.alt, TextType.IMAGE, self.image2.url),
            TextNode(self.image3.alt, TextType.IMAGE, self.image3.url),
        ]
        result = split_nodes_image([node])
        self.assertEqual(result, expected)


class Link:
    def __init__(self, raw: str):
        self.raw = raw
        self.text, self.url = re.findall(r"\[(.*?)\]\((.*?)\)", raw)[0]


class TestSplitNodesLink(unittest.TestCase):
    link1 = Link("[to boot dev](https://www.boot.dev)")
    link2 = Link("[to youtube](https://www.youtube.com/@bootdotdev)")
    link3 = Link("[example](https://example.com)")

    def test_split_nodes_link_no_link(self):
        node = TextNode("This is plain text without any links.", TextType.TEXT)
        expected = [node]
        result = split_nodes_link([node])
        self.assertEqual(result, expected)

    def test_split_nodes_link_start_link(self):
        trailing_text = " trailing text for test."
        node = TextNode(self.link1.raw + trailing_text, TextType.TEXT)
        expected = [
            TextNode(self.link1.text, TextType.LINK, self.link1.url),
            TextNode(trailing_text, TextType.TEXT),
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected)

    def test_split_nodes_link_end_link(self):
        leading_text = "leading text for test "
        node = TextNode(leading_text + self.link1.raw, TextType.TEXT)
        expected = [
            TextNode(leading_text, TextType.TEXT),
            TextNode(self.link1.text, TextType.LINK, self.link1.url),
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected)

    def test_split_nodes_link_multiple_links(self):
        node = TextNode(
            f"This is text with a link {self.link1.raw} and {self.link2.raw}",
            TextType.TEXT,
        )
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode(self.link1.text, TextType.LINK, self.link1.url),
            TextNode(" and ", TextType.TEXT),
            TextNode(self.link2.text, TextType.LINK, self.link2.url),
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected)

    def test_split_nodes_link_mixed_nodes(self):
        node1 = TextNode("This is plain text.", TextType.TEXT)
        node2 = TextNode(f"This has a {self.link1.raw}.", TextType.TEXT)
        node3 = TextNode("Another plain text.", TextType.TEXT)
        expected = [
            node1,
            TextNode("This has a ", TextType.TEXT),
            TextNode(self.link1.text, TextType.LINK, self.link1.url),
            TextNode(".", TextType.TEXT),
            node3,
        ]
        result = split_nodes_link([node1, node2, node3])
        self.assertEqual(result, expected)

    def test_split_nodes_link_consecutive_links(self):
        node = TextNode(
            f"{self.link1.raw}{self.link2.raw}{self.link3.raw}", TextType.TEXT
        )
        expected = [
            TextNode(self.link1.text, TextType.LINK, self.link1.url),
            TextNode(self.link2.text, TextType.LINK, self.link2.url),
            TextNode(self.link3.text, TextType.LINK, self.link3.url),
        ]
        result = split_nodes_link([node])
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
