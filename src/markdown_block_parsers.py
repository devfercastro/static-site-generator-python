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
def parse_code(block: str) -> HTMLNode:
    """
    Parse a markdown code block and convert it into an HTMLNode object

    Args:
        block: A string representing a markdown heading

    Returns:
        HTMLNode: An HTMLNode object representing a html "code" tag nested inside a "pre" tag

    Raises:
        ValueError: If the markdown code block is invalid
    """
    code_content = re.match(r"^(```)(.+)(```)$", block, re.DOTALL)
    if code_content:
        code_node = HTMLNode("code", code_content.group(2).strip())
        pre_node = HTMLNode("pre", None, [code_node])

        return pre_node

    raise ValueError("invalid markdown code block syntax")


# TODO: QUOTE
# TODO: UNORDERED_LIST
# TODO: ORDERED_LIST
# TODO: PARAGRAPH
