from src.core import BlockType
from .block_parser import markdown_to_blocks, block_to_block_type
from .elements import (
    parse_heading,
    parse_code,
    parse_quote,
    parse_unordered_list,
    parse_ordered_list,
    parse_paragraph,
)


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
