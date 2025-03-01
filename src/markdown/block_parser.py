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


def block_to_block_type(block: str) -> Tuple[BlockType, Union[str, Tuple[str, str]]]:
    """
    Determine the type of a markdown block

    Args:
        block: A string representing a single block of markdown

    Returns:
        BlockType: An enumerated value representing the type of the block
    """
    if match := HEADING_PATTERN.match(block):
        marker, content = match.groups()
        return BlockType.HEADING, (marker, content)

    if match := CODE_PATTERN.match(block):
        return BlockType.CODE, match.group(1)

    if match := QUOTE_PATTERN.match(block):
        return BlockType.QUOTE, match.group(1)

    if match := UNORDERED_LIST_PATTERN.findall(block):
        return BlockType.UNORDERED_LIST, match

    if match := ORDERED_LIST_PATTERN.findall(block):
        return BlockType.ORDERED_LIST, match

    return BlockType.PARAGRAPH, block
