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
        breakpoint()

        match block_type:
            case BlockType.HEADING:
                html_nodes.append(parse_heading(*block_content))  # type: ignore[reportArgumentType]
            case BlockType.CODE:
                html_nodes.append(parse_code(block_content))  # type: ignore[reportArgumentType]
            case BlockType.QUOTE:
                html_nodes.append(parse_quote(block_content))  # type: ignore[reportArgumentType]
            case BlockType.UNORDERED_LIST:
                html_nodes.append(parse_unordered_list(block_content))  # type: ignore[reportArgumentType]
            case BlockType.ORDERED_LIST:
                # TODO: must receive a list of tuples with a number and a content
                html_nodes.append(parse_ordered_list(block))  # type: ignore[reportArgumentType]
            case BlockType.PARAGRAPH:
                # TODO: must receive the content
                html_nodes.append(parse_paragraph(block))  # type: ignore[reportArgumentType]
            case _:
                raise ValueError("not matched block type")
    return html_nodes
