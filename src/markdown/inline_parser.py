from typing import List
from core import TextNode, TextType
from .elements import split_nodes_image, split_nodes_link


def split_nodes_delimiter(
    old_nodes: List[TextNode], delimiter: str, text_type: TextType
):
    """
    Split a list of TextNode using a specified delimiter and convert enclosed to a new TextNode with the passed type (text_type)

    Args:
        old_nodes: The list of TextNode to be transform
        delimiter: The sytax specifier
        text_type: The new text type to apply to enclosed segments

    Returns:
        List[TextNode]: The new list of TextNode objects resulting from the split and conversion.

    Raises:
        Exception: If a text of a TextNode has an odd number of delimiters
    """
    new_nodes: List[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            if node.text.count(delimiter) % 2 != 0:
                raise Exception(f'Unamtched delimiter "{delimiter}"')
            sections = node.text.split(delimiter)
            for i, section in enumerate(sections):
                if i % 2 == 0:  # odd parts aren't the target
                    if section != "":
                        new_nodes.append(TextNode(section, TextType.TEXT))
                else:  # even parts are the special nodes
                    new_nodes.append(TextNode(section, text_type))

    return new_nodes


def text_to_textnodes(text: str) -> List[TextNode]:
    if text == "":
        raise ValueError("cannot be empty")

    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes
