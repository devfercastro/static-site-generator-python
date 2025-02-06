import re
from typing import List, Tuple
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


def split_nodes_image(old_nodes: List[TextNode]):
    """
    Splits a list of TextNode containing markdown images into a list of TextNode where the images are separated

    Args:
        old_nodes: List of TextNode to process

    Returns:
        List[TextNode]: New list of TextNode object with images split into individual nodes
    """
    new_nodes: List[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            inline_images = extract_markdown_images(text)

            # if there are no images, skip
            if len(inline_images) == 0:
                new_nodes.append(node)
                continue

            for image in inline_images:
                image_alt = image[0]
                image_url = image[1]

                # split just once the text using the current image as delimiter
                # capture the text before and after the image
                pre_image_text, post_image_text = text.split(
                    f"![{image_alt}]({image_url})", 1
                )

                # if not empty string append the text before the image
                if pre_image_text != "":
                    new_nodes.append(TextNode(pre_image_text, TextType.TEXT))
                # then append the image (to preserve the order)
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))

                # continue with text after image
                text = post_image_text

            # append the remaining text
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: List[TextNode]):
    """
    Splits a list of TextNode containing markdown links into a list of TextNode where the links are separated

    Args:
        old_nodes: List of TextNode to process

    Returns:
        List[TextNode]: New list of TextNode object with links split into individual nodes
    """
    new_nodes: List[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            inline_links = extract_markdown_links(text)

            # if there are no links, skip
            if len(inline_links) == 0:
                new_nodes.append(node)
                continue

            for link in inline_links:
                link_text = link[0]
                link_url = link[1]

                # split just once the text using the current link as delimiter
                # capture the text before and after the link
                pre_link_text, post_link_text = text.split(
                    f"[{link_text}]({link_url})", 1
                )

                # if not empty string append before the link
                if pre_link_text != "":
                    new_nodes.append(TextNode(pre_link_text, TextType.TEXT))
                # then append the link (to preserve the order)
                new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

                # continue with text after link
                text = post_link_text

            # append the remaining text
            if text != "":
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes
