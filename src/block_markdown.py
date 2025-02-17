from enum import Enum
import re
from typing import List

from markdown_block_parsers import (
    parse_code,
    parse_heading,
    parse_paragraph,
    parse_quote,
    parse_unordered_list,
    parse_ordered_list,
)


class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"


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


def block_to_block_type(block: str) -> BlockType:
    """
    Determine the type of a markdown block

    Args:
        block: A string representing a single block of markdown

    Returns:
        BlockType: An enumerated value representing the type of the block
    """
    # a heading block must start with one to six "#" followed by a space, followed by anything
    heading_regex = r"^(#{1,6} ).+"
    # a code block must start with "```" followed by a blank character, followed by anything, followed by another blank character and ending with "```"
    code_regex = r"^(```)\s+.+\s+(```)$"
    # a quote block must start with ">" followed by a space, followed by anything
    quote_regex = r"^(> ).+"
    # an unordered list block must start with "*" or "-" followed by a space and followed by anything
    unordered_list_regex = r"^(\* |- ).+"
    # an ordered list block must start with a number followed by a ".", followed by a space and followed by anything
    ordered_list_regex = r"^([0-9]+\. ).+"

    if re.match(heading_regex, block):
        return BlockType.HEADING
    if re.match(code_regex, block):
        return BlockType.CODE
    if re.match(quote_regex, block):
        return BlockType.QUOTE
    if re.match(unordered_list_regex, block):
        return BlockType.UNORDERED_LIST
    if re.match(ordered_list_regex, block):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str):
    markdown_blocks = markdown_to_blocks(markdown)
    html_nodes = []

    for block in markdown_blocks:
        typed_block = block_to_block_type(block)
        match typed_block:
            case BlockType.HEADING:
                html_nodes.append(parse_heading(block))
            case BlockType.CODE:
                html_nodes.append(parse_code(block))
            case BlockType.QUOTE:
                html_nodes.append(parse_quote(block))
            case BlockType.UNORDERED_LIST:
                html_nodes.append(parse_unordered_list(block))
            case BlockType.ORDERED_LIST:
                html_nodes.append(parse_ordered_list(block))
            case BlockType.PARAGRAPH:
                html_nodes.append(parse_paragraph(block))
    return html_nodes
