import re
from typing import Callable, List, Literal, Tuple
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


def extract_markdown_images(text: str) -> List[Tuple[str, str]]:
    """
    Extracts the image alt text and url from inline markdown

    Args:
        text: Raw markdown text that contains the image or images

    Returns:
        List[Tuple[str, str]]: The list of tuples each one being (image alt text, image url)
    """
    regex = r"!\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)


def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
    """
    Extracts the link text and url from inline markdown

    Args:
        text: Raw markdown text that contains the link or links

    Returns:
        List[Tuple[str, str]]: The list of tuples each one beign (link text, link url)
    """
    regex = r"\[(.*?)\]\((.*?)\)"
    return re.findall(regex, text)


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
