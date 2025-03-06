import unittest

from core import LeafNode, ParentNode
from markdown.parser import markdown_to_html_node


class TestMarkdownToHtmlNodes(unittest.TestCase):
    def test_markdown_to_html_nodes(self):
        h1 = "# heading"
        code = '```\nprint("hello world")\n```'
        quote = "> Quote"
        unordered_list = "* unordered list item"
        ordered_list = "1. ordered list item"
        paragraph = "some text that represents a paragraph"
        markdown = f"""
        {h1}

        {code}

        {quote}

        {unordered_list}

        {ordered_list}

        {paragraph}
        """
        expected = [
            ParentNode(tag="h1", children=[LeafNode(None, h1.strip("# "))]),
            ParentNode("pre", [LeafNode("code", code.strip("```\n"))]),
            ParentNode(tag="blockquote", children=[LeafNode(None, quote.strip("> "))]),
            ParentNode(
                tag="ul",
                children=[
                    ParentNode(
                        tag="li", children=[LeafNode(None, unordered_list.strip("* "))]
                    )
                ],
            ),
            ParentNode(
                tag="ol",
                children=[
                    ParentNode(
                        tag="li", children=[LeafNode(None, ordered_list.strip("1. "))]
                    )
                ],
            ),
            ParentNode(tag="p", children=[LeafNode(None, paragraph)]),
        ]
        result = markdown_to_html_node(markdown)
        self.assertEqual(result, expected)
