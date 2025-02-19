import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_multiple_props(self):
        expected_result = ' href="https://www.google.com" target="_blank"'
        test_props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), expected_result)

    def test_props_to_html_with_single_prop(self):
        expected_result = ' href="https://www.google.com"'
        test_props = {
            "href": "https://www.google.com",
        }
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), expected_result)

    def test_props_to_html_with_no_props(self):
        expected_result = ""
        test_props = None
        node = HTMLNode(props=test_props)
        self.assertEqual(node.props_to_html(), expected_result)
