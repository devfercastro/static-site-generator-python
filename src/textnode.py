from enum import Enum


class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"


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
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
