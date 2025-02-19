import unittest
from block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)
from htmlnode import HTMLNode


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks_multiple(self):
        markdown = """
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item
        """
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_empty_input(self):
        markdown = ""
        expected = []
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_single_paragraph(self):
        markdown = "This is a single paragraph."
        expected = ["This is a single paragraph."]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)

    def test_markdown_to_blocks_multiple_empty_lines(self):
        markdown = "\n\n\n# Heading\n\n\nThis is a paragraph.\n\n\n"
        expected = ["# Heading", "This is a paragraph."]
        result = markdown_to_blocks(markdown)
        self.assertEqual(result, expected)


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_multiple_blocks(self):
        markdown = """
        # heading

        ```
        print("hello world")
        ```

        > Quote

        * unordered list item

        - unordered list item option two

        1. ordered list item

        paragraph
        """
        expected = [
            BlockType.HEADING,
            BlockType.CODE,
            BlockType.QUOTE,
            BlockType.UNORDERED_LIST,
            BlockType.UNORDERED_LIST,
            BlockType.ORDERED_LIST,
            BlockType.PARAGRAPH,
        ]
        results = list(
            map(lambda block: block_to_block_type(block), markdown_to_blocks(markdown))
        )
        self.assertEqual(results, expected)

    def test_block_to_block_type_heading(self):
        block = "# This is a heading"
        expected = BlockType.HEADING
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

    def test_block_to_block_type_code(self):
        block = "```\nprint('Hello, World!')\n```"
        expected = BlockType.CODE
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

    def test_block_to_block_type_quote(self):
        block = "> This is a quote"
        expected = BlockType.QUOTE
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

    def test_block_to_block_type_unordered_list(self):
        block = "* This is an unordered list item"
        expected = BlockType.UNORDERED_LIST
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list(self):
        block = "1. This is an ordered list item"
        expected = BlockType.ORDERED_LIST
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

    def test_block_to_block_type_paragraph(self):
        block = "This is a simple paragraph."
        expected = BlockType.PARAGRAPH
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

    def test_block_to_block_type_empty_string(self):
        block = ""
        expected = BlockType.PARAGRAPH
        result = block_to_block_type(block)
        self.assertEqual(result, expected)


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


if __name__ == "__main__":
    unittest.main()
