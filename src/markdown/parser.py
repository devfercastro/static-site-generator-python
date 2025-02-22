from typing import List

from core.htmlnode import HTMLNode
from core import BlockType

from .block_parser import block_to_block_type, markdown_to_blocks
from .elements import (
    parse_code,
    parse_heading,
    parse_ordered_list,
    parse_paragraph,
    parse_quote,
    parse_unordered_list,
)


def markdown_to_html_node(markdown: str) -> List[HTMLNode]:
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
