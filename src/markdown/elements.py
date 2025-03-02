from typing import Callable, List, Literal, Tuple

from src.core import ParentNode, TextNode, TextType
from src.core.leafnode import LeafNode

from .extractor import extract_markdown_images, extract_markdown_links


def parse_heading(marker: str, content: str) -> LeafNode:
    """Parse a markdown heading and convert it to an HTMLNode object

    Args:
        marker: The string of the marker
        content: The header text

    Returns:
        HTMLNode: An HTMLNode object representing a html header

    """
    level = len(marker)

    return LeafNode(tag=f"h{level}", value=content)


def parse_code(content: str) -> ParentNode:
    """Parse a markdown code block into an HTMLNode object

    Args:
        content: The content of the code block

    Returns:
        HTMLNode: An HTMLNode object representing a html "code" tag nested inside a "pre" tag

    """
    return ParentNode(tag="pre", children=[LeafNode("code", content)])


def parse_quote(content: str) -> LeafNode:
    """Parse the content of a markdown quote into an HTMLNode object

    Args:
        content: The content of the quote

    Returns:
        HTMLNode: An HTMLNode object representing a html "blockquote" tag

    """
    return LeafNode(tag="blockquote", value=content)


def parse_unordered_list(list_items: List[str]) -> ParentNode:
    """Parse the list items of a markdown unordered list into an HTMLNode object

    Args:
        list_items: The list items of the unordered list

    Returns:
        HTMLNode: An HTMLNode object representing several "li" tags nested inside a "ul" tag

    """
    li_nodes = [
        ParentNode(tag="li", children=[LeafNode(None, content)])
        for content in list_items
    ]

    return ParentNode(tag="ul", children=li_nodes)  # type: ignore[reportArgumentType]


def parse_ordered_list(list_items: List[Tuple[str, str]]) -> ParentNode:
    """Parse the list items of a markdown ordered list into an HTMLNode object

    Args:
        list_items: The list items of the ordered list

    Returns:
        HTMLNode: An HTMLNode object representing several "li" tags nested inside a "ol" tag

    """
    li_nodes = [
        ParentNode(tag="li", children=[LeafNode(None, content)])
        # get just content, ignore number
        for _, content in list_items
    ]

    return ParentNode(tag="ol", children=li_nodes)  # type: ignore[reportArgumentType]


def parse_paragraph(content: str) -> LeafNode:
    """Parse a markdown paragraph into an HTMLNode object

    Args:
        content: The content of the paragraph

    Returns:
        HTMLNode: An HTMLNode object representing a "p" tag

    """
    return LeafNode(tag="p", value=content)


def split_nodes(
    old_nodes: List[TextNode],
    extractor: Callable[[str], List[Tuple[str, str]]],
    node_type: Literal[TextType.IMAGE, TextType.LINK],
):
    """
    Generic function to split TextNode objects based on a delimiter extractor

    Args:
        old_nodes: List of TextNode to process
        extractor: Function to extract the markdown elements (e.g, link or images)
        node_type: Type of TextNode to create for the extracted elements

    Returns:
        List[TextNode]: New list of TextNode objects with the extracted elements split
    """
    new_nodes: List[TextNode] = []

    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            # non-text nodes are preserved
            new_nodes.append(old_node)
            continue

        text = old_node.text
        elements = extractor(old_node.text)

        # if no elements are found, preserve the original
        if len(elements) == 0:
            new_nodes.append(old_node)
            continue

        # process each extracted element
        for element in elements:
            el_text, el_url = element

            # the delimiter change depending if it's an image or a link
            element_delimiter = (
                f"![{el_text}]({el_url})"
                if node_type == TextType.IMAGE
                else f"[{el_text}]({el_url})"
            )

            # split the text using and capture the pre and post text
            pre_element_text, post_element_text = text.split(element_delimiter)

            # append the text before the element
            if pre_element_text != "":
                new_nodes.append(TextNode(pre_element_text, TextType.TEXT))
            # append the element
            new_nodes.append(TextNode(el_text, node_type, el_url))

            # continue processing the text after the element
            text = post_element_text

        # append any remaining text after processing all elements
        if text != "":
            new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_image(old_nodes: List[TextNode]):
    """
    Splits a list of TextNode containing markdown images into a list of TextNode where the images are separated

    Args:
        old_nodes: List of TextNode to process

    Returns:
        List[TextNode]: New list of TextNode object with images split into individual nodes
    """
    return split_nodes(old_nodes, extract_markdown_images, TextType.IMAGE)


def split_nodes_link(old_nodes: List[TextNode]):
    """
    Splits a list of TextNode containing markdown links into a list of TextNode where the links are separated

    Args:
        old_nodes: List of TextNode to process

    Returns:
        List[TextNode]: New list of TextNode object with links split into individual nodes
    """
    return split_nodes(old_nodes, extract_markdown_links, TextType.LINK)
