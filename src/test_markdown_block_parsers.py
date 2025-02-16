import unittest
from textwrap import dedent

from markdown_block_parsers import parse_code, parse_heading, parse_quote
from htmlnode import HTMLNode


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
