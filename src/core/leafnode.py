from typing import Dict

from .htmlnode import HTMLNode


class LeafNode(HTMLNode):
    """Represents a single HTML tag with no children. For example, a simple `<p>` tag."""

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: Dict[str, str | None] | None = None,
    ) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        """Renders a leaf node as an HTML string"""
        props_parsed = self.props_to_html()

        if self.tag == "img":
            return f"<{self.tag}{props_parsed}>"

        if self.value is None:
            raise ValueError("Leaf node must have a value")
        if self.tag is None:
            return self.value

        return f"<{self.tag}{props_parsed}>{self.value}</{self.tag}>"
