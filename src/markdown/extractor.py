import re
from typing import List, Tuple


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
