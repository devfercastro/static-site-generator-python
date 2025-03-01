from typing import List, Tuple, Union

from src.core import BlockType

from .constants import (
    CODE_PATTERN,
    HEADING_PATTERN,
    ORDERED_LIST_PATTERN,
    QUOTE_PATTERN,
    UNORDERED_LIST_PATTERN,
)


def markdown_to_blocks(markdown: str) -> List[str]:
    """
    Converts a markdown string into a list of blocks

    Args:
        markdown: A string containing markdown text

    Returns:
        List[str]: A list of string, where each string is a block of markdown. Blocks are seperated by a blank line
    """
    blocks = []

    for block in markdown.split("\n\n"):
        stripped_block = block.strip()

        if stripped_block != "":
            # handle blocks with multiple indentated lines
            if "\n" in stripped_block:
                # remove indentation from each line
                outdented_lines = [line.strip() for line in stripped_block.split("\n")]
                blocks.append("\n".join(outdented_lines))

            else:
                # simple blocks just appends it
                blocks.append(stripped_block)

    return blocks


# Type aliases for clarity
HeadingData = Tuple[str, str]  # (marker, content)
CodeData = str  # Code content
QuoteData = str  # Quote content
UnorderedListData = List[str]  # List of item contents
OrderedListData = List[Tuple[str, str]]  # List of (number, content)
ParagraphData = str  # Entire block as paragraph
BlockData = Union[
    HeadingData, CodeData, QuoteData, UnorderedListData, OrderedListData, ParagraphData
]


def block_to_block_type(block: str) -> Tuple[BlockType, BlockData]:
    """
    Determine the type of a markdown block and extract associated data.

    Args:
        block: A string representing a single block of markdown.

    Returns:
        A tuple containing:
        - BlockType: An enumerated value representing the type of the block.
        - Associated data, which depends on the block type:
            - BlockType.HEADING: Tuple[str, str] - (marker, content), where marker is the heading level (e.g., "##")
              and content is the heading text.
            - BlockType.CODE: str - The content within the code block.
            - BlockType.QUOTE: str - The content of the quote block.
            - BlockType.UNORDERED_LIST: List[str] - A list of strings, each being the content of an unordered list item.
            - BlockType.ORDERED_LIST: List[Tuple[str, str]] - A list of tuples, each containing (number, content),
              where number is the item number as a string and content is the item text.
            - BlockType.PARAGRAPH: str - The entire block as a string, if no other patterns match.
    """
    # Check if the block is a heading (e.g., "## Heading")
    if match := HEADING_PATTERN.match(block):
        marker, content = match.groups()  # Extract marker (e.g., "##") and content
        return BlockType.HEADING, (marker, content)

    # Check if the block is a code block (e.g., ```\ncode\n```)
    if match := CODE_PATTERN.match(block):
        return BlockType.CODE, match.group(1)  # Extract the code content

    # Check if the block is a quote (e.g., "> Quote text")
    if match := QUOTE_PATTERN.match(block):
        return BlockType.QUOTE, match.group(1)  # Extract the quote content

    # Check if the block contains unordered list items (e.g., "- Item")
    if match := UNORDERED_LIST_PATTERN.findall(block):
        return BlockType.UNORDERED_LIST, match  # Returns list of item contents

    # Check if the block contains ordered list items (e.g., "1. Item")
    if match := ORDERED_LIST_PATTERN.findall(block):
        return BlockType.ORDERED_LIST, match  # Returns list of (number, content) tuples

    # Default case: if no patterns match, treat the block as a paragraph
    return BlockType.PARAGRAPH, block
