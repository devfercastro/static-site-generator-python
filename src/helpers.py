from typing import List
from textnode import TextNode, TextType
from leafnode import LeafNode


def text_node_to_html_node(text_node: TextNode):
    """
    Converts a TextNode to an LeafNode
    Args:
        text_node: The text object to be converted
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
    It takes a list of "old nodes", a delimiter, and a text type. Returns a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax.
    Args:
        old_nodes: The list of nodes to be transform
        delimiter: The sytax specifier
        text_type: The type of the node within the delimiters

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
                if i % 2 == 0:
                    if part:
                        new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))

    return new_nodes
