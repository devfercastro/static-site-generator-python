from typing import List

from src.core import BlockType, HTMLNode

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
        block_type, block_content = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                # TODO: must receive the marker and the content
                breakpoint()
                html_nodes.append(parse_heading(*block_content))
            case BlockType.CODE:
                # TODO: must receive the content
                html_nodes.append(parse_code(block))
            case BlockType.QUOTE:
                # TODO: must receive the content
                html_nodes.append(parse_quote(block))
            case BlockType.UNORDERED_LIST:
                # TODO: must receive a list of contents
                html_nodes.append(parse_unordered_list(block))
            case BlockType.ORDERED_LIST:
                # TODO: must receive a list of tuples with a number and a content
                html_nodes.append(parse_ordered_list(block))
            case BlockType.PARAGRAPH:
                # TODO: must receive the content
                html_nodes.append(parse_paragraph(block))
            case _:
                raise ValueError("not matched block type")
    return html_nodes
