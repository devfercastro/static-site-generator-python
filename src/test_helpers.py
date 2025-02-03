import unittest

from helpers import split_nodes_delimiter, text_node_to_html_node
from textnode import TextNode, TextType
from leafnode import LeafNode


class TestTextNodeToHtmlNode(unittest.TestCase):
    def test_text(self):
        text = "Hello, world!"
        node = TextNode(text, TextType.TEXT)
        html_node = text_node_to_html_node(node)
        expected = LeafNode(tag=None, value=text)
        self.assertEqual(html_node, expected)

    def test_bold(self):
        text = "Bold text"
        node = TextNode(text, TextType.BOLD)
        html_node = text_node_to_html_node(node)
        expected = LeafNode(tag="b", value=text)
        self.assertEqual(html_node, expected)

    def test_italic(self):
        text = "Italic text"
        node = TextNode(text, TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        expected = LeafNode(tag="i", value=text)
        self.assertEqual(html_node, expected)

    def test_code(self):
        text = "print('Hello')"
        node = TextNode(text, TextType.CODE)
        html_node = text_node_to_html_node(node)
        expected = LeafNode(tag="code", value=text)
        self.assertEqual(html_node, expected)

    def test_link(self):
        text = "Click here"
        url = "https://example.com"
        node = TextNode(text, TextType.LINK, url)
        html_node = text_node_to_html_node(node)
        expected = LeafNode(tag="a", value=text, props={"href": url})
        self.assertEqual(html_node, expected)

    def test_image(self):
        alt_text = "An image"
        url = "https://example.com/image.png"
        node = TextNode(alt_text, TextType.IMAGE, url)
        html_node = text_node_to_html_node(node)
        expected = LeafNode(tag="img", value="", props={"src": url, "alt": alt_text})
        self.assertEqual(html_node, expected)

    def test_invalid_text_type(self):
        node = TextNode("Invalid", "invalid")  # deliberately wrong type
        with self.assertRaises(Exception) as context:
            text_node_to_html_node(node)
        self.assertIn("Incorrect text type", str(context.exception))


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


if __name__ == "__main__":
    unittest.main()
