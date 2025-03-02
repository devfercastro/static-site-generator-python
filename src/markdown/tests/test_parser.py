import unittest

from src.core import LeafNode, ParentNode
from src.markdown.parser import markdown_to_html_node


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
            LeafNode("h1", h1.strip("# ")),
            ParentNode("pre", [LeafNode("code", code.strip("```\n"))]),
            LeafNode("blockquote", quote.strip("> ")),
            ParentNode("ul", [LeafNode("li", unordered_list.strip("* "))]),
            ParentNode("ol", [LeafNode("li", ordered_list.strip("1. "))]),
            LeafNode("p", paragraph),
        ]
        result = markdown_to_html_node(markdown)
        self.assertEqual(result, expected)
