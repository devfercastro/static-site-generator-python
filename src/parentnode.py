from typing import Dict, List
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str | None = None,
        children: List["HTMLNode"] | None = None,
        props: Dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self) -> str:
        if not self.tag:
            raise ValueError("ParentNode must have a tag")
        if not self.children:
            raise ValueError("ParentNode must have childrens")
        content = ""
        for node in self.children:
            content += node.to_html()

        return f"<{self.tag}>{content}</{self.tag}>"
