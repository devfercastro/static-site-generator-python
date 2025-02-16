import re
from htmlnode import HTMLNode


def parse_heading(block: str) -> HTMLNode:
    """
    Parse a markdown heading and convert it to an HTMLNode object

    Args:
        block: A string representing a markdown heading.

    Returns:
        HTMLNode: An HTMLNode object representing a html header

    Raises:
        ValueError: If the markdown heading is invalid
    """
    heading_type = block.count("#")
    heading_content = re.match(r"#{1,6} (.+)", block)
    if heading_content:
        return HTMLNode(f"h{heading_type}", heading_content.group(1))

    raise ValueError("invalid markdown header syntax")


# TODO: CODE
# TODO: QUOTE
# TODO: UNORDERED_LIST
# TODO: ORDERED_LIST
# TODO: PARAGRAPH
