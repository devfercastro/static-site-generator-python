from enum import Enum
import re
from typing import List


def markdown_to_blocks(markdown: str) -> List[str]:
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


class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDEREDLIST = "unordered_list"
    ORDEREDLIST = "ordered_list"
    PARAGRAPH = "paragraph"


def block_to_block_type(block: str) -> BlockType:
    heading_regex = r"^(#{1,6} ).+"
    code_regex = r"^(```)\s+.+\s+(```)$"
    quote_regex = r"^(> ).+"
    unordered_list_regex = r"^(\* |- ).+"
    ordered_list_regex = r"^([0-9]. ).+"

    if re.match(heading_regex, block):
        return BlockType.HEADING
    if re.match(code_regex, block):
        return BlockType.CODE
    if re.match(quote_regex, block):
        return BlockType.QUOTE
    if re.match(unordered_list_regex, block):
        return BlockType.UNORDEREDLIST
    if re.match(ordered_list_regex, block):
        return BlockType.ORDEREDLIST

    return BlockType.PARAGRAPH
