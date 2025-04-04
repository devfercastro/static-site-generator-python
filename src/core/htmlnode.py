from typing import Dict, List


class HTMLNode:
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: List["HTMLNode"] | None = None,
        props: Dict[str, str | None] | None = None,
    ) -> None:
        """
        Args:
            tag: A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
            value: A string representing the value of the HTML tag (e.g. the text inside a paragraph)
            children: A list of HTMLNode objects representing the children of this node
            props: A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError("This method should be overriden by child classes.")

    def props_to_html(self) -> str:
        """
        Returns a string that represents the HTML attributes of the node.
        """
        if self.props:
            leading_space = " "
            return leading_space + " ".join(
                f'{key}="{value}"' for key, value in self.props.items()
            )
        return ""

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, HTMLNode):
            raise ValueError("Must be HTMLNode instance")
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )
