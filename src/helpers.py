from typing import List
from textnode import TextNode, TextType
from leafnode import LeafNode


def text_node_to_html_node(text_node: TextNode):
    """
    Converts a TextNode to a corresponding LeafNode

    Args:
        text_node: The TextNode instances to be converted

    Return:
        LeafNode: The new LeafNode with the corresponding opts

    Raises:
        Exception: If the text_node has an unrecognized text type
    """
    out = None
    match text_node.text_type:
        case TextType.TEXT:
            out = LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            out = LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            out = LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            out = LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            out = LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            out = LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            raise Exception("Incorrect text type")
    return out


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
            parts = node.text.split(delimiter)

            for i, part in enumerate(parts):
                if i % 2 == 0:  # odd parts aren't the target
                    if part:
                        new_nodes.append(TextNode(part, TextType.TEXT))
                else:  # even parts are the special nodes
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes
