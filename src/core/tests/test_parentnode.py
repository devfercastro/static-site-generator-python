import unittest

from src.core.parentnode import ParentNode
from src.core.leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_invalid_parentnode_no_tag(self):
        node = ParentNode(
            tag=None,
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have a tag")

    def test_invalid_parentnode_no_children(self):
        node = ParentNode(
            tag="p",
            children=None,
        )
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception),
                         "ParentNode must have childrens")

    def test_invalid_parentnode_nested_no_tag(self):
        inner_parent = ParentNode(
            tag=None,
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        outer_parent = ParentNode(tag="div", children=[inner_parent])
        with self.assertRaises(ValueError) as context:
            outer_parent.to_html()
        self.assertEqual(str(context.exception), "ParentNode must have a tag")

    def test_invalid_parentnode_nested_no_children(self):
        inner_parent = ParentNode(tag="p", children=None)
        outer_parent = ParentNode(tag="div", children=[inner_parent])
        with self.assertRaises(ValueError) as context:
            outer_parent.to_html()
        self.assertEqual(str(context.exception),
                         "ParentNode must have childrens")

    def test_valid_parentnode_multiple_childrens_no_props(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_valid_parentnode_nested(self):
        inner_parent = ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        outer_parent = ParentNode(tag="div", children=[inner_parent])
        expected = (
            "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></div>"
        )
        self.assertEqual(outer_parent.to_html(), expected)

    def test_valid_parentnode_nesting_multiple(self):
        inner_parent = ParentNode(
            tag="p",
            children=[
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        inner_parent2 = ParentNode(
            tag="p",
            children=[LeafNode("b", "Bold text"),
                      LeafNode(None, "Normal text")],
        )
        outer_parent = ParentNode(
            tag="div", children=[inner_parent, inner_parent2])
        expected = "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><p><b>Bold text</b>Normal text</p></div>"
        self.assertEqual(outer_parent.to_html(), expected)

    def test_valid_parentnode_nested_multiple_levels(self):
        innermost_parent = ParentNode(
            tag="span",
            children=[LeafNode("b", "Bold text"),
                      LeafNode(None, "Normal text")],
        )
        inner_parent = ParentNode(tag="p", children=[innermost_parent])
        outer_parent = ParentNode(tag="div", children=[inner_parent])
        expected = "<div><p><span><b>Bold text</b>Normal text</span></p></div>"
        self.assertEqual(outer_parent.to_html(), expected)
