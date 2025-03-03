import unittest

from core import BlockType
from markdown.block_parser import block_to_block_type, markdown_to_blocks


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
            map(
                lambda block: block_to_block_type(block)[0],
                markdown_to_blocks(markdown),
            )
        )
        self.assertEqual(results, expected)

    def test_block_to_block_type_heading(self):
        marker = "##"
        content = "This is a h2 header"
        block = f"{marker} {content}"
        expected = (BlockType.HEADING, (marker, content))
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

    def test_block_to_block_type_code(self):
        code = "print('Hello World!')"
        block = f"```\n{code}\n```"
        expected = (BlockType.CODE, code)
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

    def test_block_to_block_type_quote(self):
        content = "This is a quote"
        block = f"> {content}"
        expected = (BlockType.QUOTE, content)
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

    def test_block_to_block_type_unordered_list(self):
        content = "This is an unordered list item"
        block = f"* {content}"
        expected = (BlockType.UNORDERED_LIST, [content])
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

    def test_block_to_block_type_ordered_list(self):
        number = "1"
        content = "This is the first item in an ordered list"
        block = f"{number}. {content}"
        expected = BlockType.ORDERED_LIST, [(number, content)]
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

    def test_block_to_block_type_paragraph(self):
        block = "This is a simple paragraph."
        expected = (BlockType.PARAGRAPH, block)
        result = block_to_block_type(block)
        self.assertEqual(result, expected)

    def test_block_to_block_type_empty_string(self):
        block = ""
        expected = BlockType.PARAGRAPH, ""
        result = block_to_block_type(block)
        self.assertEqual(result, expected)
