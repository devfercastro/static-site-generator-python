import unittest
from src.markdown.parser import markdown_to_html_node
from src.core import HTMLNode


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
            HTMLNode("h1", h1.strip("# ")),
            HTMLNode("pre", None, [HTMLNode("code", code.strip("```\n"))]),
            HTMLNode("blockquote", quote.strip("> ")),
            HTMLNode("ul", None, [HTMLNode("li", unordered_list.strip("* "))]),
            HTMLNode("ol", None, [HTMLNode("li", ordered_list.strip("1. "))]),
            HTMLNode("p", paragraph),
        ]
        result = markdown_to_html_node(markdown)
        self.assertEqual(result, expected)
