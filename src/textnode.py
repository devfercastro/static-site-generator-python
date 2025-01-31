from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        """
        Args:
            text: The text content of the node.
            text_type: The type of text this node contains, which is a member of the TextType enum.
            url: The URL of the link or image, if the text is a link. Default to None if nothing is passed in.
        """
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            raise ValueError("Must be TextNode instances")
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode(text={self.text!r}, text_type={self.text_type.value!r}, url={self.url!r})"


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
