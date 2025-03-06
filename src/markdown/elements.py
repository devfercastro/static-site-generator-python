from typing import Callable, List, Literal, Tuple

from core import ParentNode, LeafNode, TextNode, TextType
from markdown.inline_parser import text_to_textnodes

from .extractor import extract_markdown_images, extract_markdown_links


def parse_inline(inline_content: str, exclude: List[TextType] = []) -> List[LeafNode]:
    """Converts inline content into a list of LeafNode objects representing HTML elements.

    Args:
        inline_content: The string containing inline content to be parsed

    Returns:
        List[LeafNode]: A list of LeafNode objects representing the structured content.

    """
    # extract the text nodes: bold, italic, images, links, etc.
    text_nodes = text_to_textnodes(inline_content)
    parsed_nodes: List[LeafNode] = []

    # for each text node
    for node in text_nodes:
        content = None
        tag = None
        props = None

        # if it's specify to be excluded or it's just normal text, append it as a normal text html leaf node
        if node.text_type in exclude or node.text_type == TextType.TEXT:
            parsed_nodes.append(LeafNode(None, node.text))
            continue

        # otherwise append as a special html node
        match node.text_type:
            case TextType.BOLD:
                tag = "b"
                content = node.text
            case TextType.ITALIC:
                tag = "i"
                content = node.text
            case TextType.CODE:
                tag = "code"
                content = node.text
            case TextType.LINK:
                tag = "a"
                content = node.text
                props = {"href": node.url}
            # Not needed
            # case TextType.IMAGE:
            #     tag = "img"
            #     props = {"src": node.url, "alt": node.text}
            #

        parsed_nodes.append(LeafNode(tag, content, props))

    return parsed_nodes


def parse_heading(marker: str, content: str):
    """Parse a markdown heading and convert it to an ParentNode object

    Args:
        marker: The string of the marker
        content: The header text

    Returns:
        ParentNode: An ParentNode object representing a html header

    """
    level = len(marker)

    return ParentNode(tag=f"h{level}", children=parse_inline(content))


def parse_code(content: str):
    """Parse a markdown code block into an ParentNode object

    Args:
        content: The content of the code block

    Returns:
        ParentNode: An ParentNode object representing a html "code" tag nested inside a "pre" tag

    """
    return ParentNode(tag="pre", children=[LeafNode("code", content)])


def parse_quote(content: str):
    """Parse the content of a markdown quote into an ParentNode object

    Args:
        content: The content of the quote

    Returns:
        ParentNode: An ParentNode object representing a html "blockquote" tag

    """
    return ParentNode(tag="blockquote", children=parse_inline(content))


def parse_unordered_list(list_items: List[str]):
    """Parse the list items of a markdown unordered list into an ParentNode object

    Args:
        list_items: The list items of the unordered list without the marker

    Returns:
        ParentNode: An ParentNode object representing several "li" tags nested inside a "ul" tag

    """
    li_nodes = [
        ParentNode(tag="li", children=parse_inline(content)) for content in list_items
    ]

    return ParentNode(tag="ul", children=li_nodes)


def parse_ordered_list(list_items: List[Tuple[str, str]]):
    """Parse the list items of a markdown ordered list into an ParentNode object

    Args:
        list_items: The list items of the ordered list

    Returns:
        ParentNode: An ParentNode object representing several "li" tags nested inside a "ol" tag

    """
    li_nodes = [
        ParentNode(tag="li", children=parse_inline(content))
        # get just content, ignore number
        for _, content in list_items
    ]

    return ParentNode(tag="ol", children=li_nodes)


def parse_paragraph(content: str):
    """Parse a markdown paragraph into an ParentNode object

    Args:
        content: The content of the paragraph

    Returns:
        ParentNode: An ParentNode object representing a "p" tag

    """
    return ParentNode(tag="p", children=parse_inline(content))


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
