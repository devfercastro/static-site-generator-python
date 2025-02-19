from .htmlnode import HTMLNode
from typing import Dict


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        props: Dict[str, str | None] | None = None,
    ) -> None:
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self) -> str:
        """
        Renders a leaf node as an HTML string
        """
        if self.value is None:
            raise ValueError("Leaf node must have a value")
        if self.tag is None:
            return self.value

        props_parsed = self.props_to_html()
        return f"<{self.tag}{props_parsed}>{self.value}</{self.tag}>"
