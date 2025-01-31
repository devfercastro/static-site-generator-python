import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from leafnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_dif_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_dif_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.CODE)
        self.assertNotEqual(node, node2)

    def test_dif_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://url1")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://url2")
        self.assertNotEqual(node, node2)


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


if __name__ == "__main__":
    unittest.main()
