import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_valid_leaf_node_no_props(self):
        node = LeafNode(tag="p", value="This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        self.assertEqual(node.to_html(), expected)

    def test_valid_leaf_node_with_props(self):
        node = LeafNode(
            tag="a", value="Click me!", props={"href": "https://www.google.com"}
        )
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)

    def test_valid_leaf_node_raw_text(self):
        node = LeafNode(value="This is a text node.")
        expected = "This is a text node."
        self.assertEqual(node.to_html(), expected)

    def test_invalid_leaf_node_no_value(self):
        node = LeafNode(
            tag="p",
        )
        with self.assertRaises(ValueError):
            print(node.to_html())
