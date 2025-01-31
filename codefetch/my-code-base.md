main.sh
```
1 | python3 src/main.py
```

public/index.html
```
1 | <html>
2 | <head>
3 |     <title>Why Frontend Development Sucks</title>
4 |     <link rel="stylesheet" href="styles.css">
5 | </head>
6 | <body>
7 |     <h1>Front-end Development is the Worst</h1>
8 |     <p>
9 |         Look, front-end development is for script kiddies and soydevs who can't handle the real programming. I mean,
10 |         it's just a bunch of divs and spans, right? And css??? It's like, "Oh, I want this to be red, but not thaaaaat
11 |         red." What a joke.
12 |     </p>
13 |     <p>
14 |         Real programmers code, not silly markup languages. They code on Arch Linux, not macOS, and certainly not
15 |         Windows. They use Vim, not VS Code. They use C, not HTML. Come to the
16 |         <a href="https://www.boot.dev">backend</a>, where the real programming
17 |         happens.
18 |     </p>
19 | </body>
20 | </html>
```

public/styles.css
```
1 | body {
2 |     font-family: Arial, sans-serif;
3 |     line-height: 1.6;
4 |     margin: 0;
5 |     padding: 0;
6 |     background-color: #1f1f23;
7 | }
8 | body {
9 |     max-width: 600px;
10 |     margin: 0 auto;
11 |     padding: 20px;
12 | }
13 | h1 {
14 |     color: #ffffff;
15 |     margin-bottom: 20px;
16 | }
17 | p {
18 |     color: #999999;
19 |     margin-bottom: 20px;
20 | }
21 | a {
22 |     color: #6568ff;
23 | }
```

src/htmlnode.py
```
1 | from typing import Dict, List
2 | 
3 | 
4 | class HTMLNode:
5 |     def __init__(
6 |         self,
7 |         tag: str | None = None,
8 |         value: str | None = None,
9 |         children: List["HTMLNode"] | None = None,
10 |         props: Dict[str, str] | None = None,
11 |     ) -> None:
12 |         """
13 |         Args:
14 |             tag: A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
15 |             value: A string representing the value of the HTML tag (e.g. the text inside a paragraph)
16 |             children: A list of HTMLNode objects representing the children of this node
17 |             props: A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}
18 |         """
19 |         # TODO: if no tag render raw text
20 |         # TODO: if no value assume it has children
21 |         # TODO: if no children assume it just has value
22 |         # TODO: if no props assume it has no attributes
23 |         self.tag = tag
24 |         self.value = value
25 |         self.children = children
26 |         self.props = props
27 | 
28 |     def to_html(self) -> str:
29 |         raise NotImplementedError("This method should be overriden by child classes.")
30 | 
31 |     def props_to_html(self) -> str:
32 |         """
33 |         Returns a string that represents the HTML attributes of the node.
34 |         """
35 |         if self.props:
36 |             leading_space = " "
37 |             return leading_space + " ".join(
38 |                 f'{key}="{value}"' for key, value in self.props.items()
39 |             )
40 |         return ""
41 | 
42 |     def __repr__(self) -> str:
43 |         return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"
```

src/leafnode.py
```
1 | from htmlnode import HTMLNode
2 | from typing import Dict
3 | 
4 | 
5 | class LeafNode(HTMLNode):
6 |     def __init__(
7 |         self,
8 |         tag: str | None = None,
9 |         value: str | None = None,
10 |         props: Dict[str, str] | None = None,
11 |     ) -> None:
12 |         super().__init__(tag=tag, value=value, children=None, props=props)
13 | 
14 |     def to_html(self) -> str:
15 |         """
16 |         Renders a leaf node as an HTML string
17 |         """
18 |         if self.value is None:
19 |             raise ValueError("Leaf node must have a value")
20 |         if self.tag is None:
21 |             return self.value
22 | 
23 |         props_parsed = self.props_to_html()
24 |         return f"<{self.tag}{props_parsed}>{self.value}</{self.tag}>"
```

src/main.py
```
1 | from textnode import TextNode, TextType
2 | 
3 | 
4 | def main():
5 |     dummy_obj = TextNode("fañsdkljfa", TextType.BOLD, "https://nose")
6 |     print(dummy_obj)
7 | 
8 | 
9 | if __name__ == "__main__":
10 |     main()
```

src/test_htmlnode.py
```
1 | import unittest
2 | 
3 | from htmlnode import HTMLNode
4 | 
5 | 
6 | class TestHTMLNode(unittest.TestCase):
7 |     def test_props_to_html_with_multiple_props(self):
8 |         expected_result = ' href="https://www.google.com" target="_blank"'
9 |         test_props = {
10 |             "href": "https://www.google.com",
11 |             "target": "_blank",
12 |         }
13 |         node = HTMLNode(props=test_props)
14 |         self.assertEqual(node.props_to_html(), expected_result)
15 | 
16 |     def test_props_to_html_with_single_prop(self):
17 |         expected_result = ' href="https://www.google.com"'
18 |         test_props = {
19 |             "href": "https://www.google.com",
20 |         }
21 |         node = HTMLNode(props=test_props)
22 |         self.assertEqual(node.props_to_html(), expected_result)
23 | 
24 |     def test_props_to_html_with_no_props(self):
25 |         expected_result = ""
26 |         test_props = None
27 |         node = HTMLNode(props=test_props)
28 |         self.assertEqual(node.props_to_html(), expected_result)
```

src/test_leafnode.py
```
1 | import unittest
2 | 
3 | from leafnode import LeafNode
4 | 
5 | 
6 | class TestLeafNode(unittest.TestCase):
7 |     def test_valid_leaf_node_no_props(self):
8 |         node = LeafNode(tag="p", value="This is a paragraph of text.")
9 |         expected = "<p>This is a paragraph of text.</p>"
10 |         self.assertEqual(node.to_html(), expected)
11 | 
12 |     def test_valid_leaf_node_with_props(self):
13 |         node = LeafNode(
14 |             tag="a", value="Click me!", props={"href": "https://www.google.com"}
15 |         )
16 |         expected = '<a href="https://www.google.com">Click me!</a>'
17 |         self.assertEqual(node.to_html(), expected)
18 | 
19 |     def test_valid_leaf_node_raw_text(self):
20 |         node = LeafNode(value="This is a text node.")
21 |         expected = "This is a text node."
22 |         self.assertEqual(node.to_html(), expected)
23 | 
24 |     def test_invalid_leaf_node_no_value(self):
25 |         node = LeafNode(
26 |             tag="p",
27 |         )
28 |         with self.assertRaises(ValueError):
29 |             print(node.to_html())
```

src/test_textnode.py
```
1 | import unittest
2 | 
3 | from textnode import TextNode, TextType
4 | 
5 | 
6 | class TestTextNode(unittest.TestCase):
7 |     def test_eq(self):
8 |         node = TextNode("This is a text node", TextType.BOLD)
9 |         node2 = TextNode("This is a text node", TextType.BOLD)
10 |         self.assertEqual(node, node2)
11 | 
12 |     def test_dif_text(self):
13 |         node = TextNode("This is a text node", TextType.BOLD)
14 |         node2 = TextNode("This is a different text node", TextType.BOLD)
15 |         self.assertNotEqual(node, node2)
16 | 
17 |     def test_dif_type(self):
18 |         node = TextNode("This is a text node", TextType.BOLD)
19 |         node2 = TextNode("This is a text node", TextType.CODE)
20 |         self.assertNotEqual(node, node2)
21 | 
22 |     def test_dif_url(self):
23 |         node = TextNode("This is a text node", TextType.BOLD, "https://url1")
24 |         node2 = TextNode("This is a text node", TextType.BOLD, "https://url2")
25 |         self.assertNotEqual(node, node2)
26 | 
27 | 
28 | if __name__ == "__main__":
29 |     unittest.main()
```

src/textnode.py
```
1 | from enum import Enum
2 | 
3 | 
4 | class TextType(Enum):
5 |     NORMAL = "normal"
6 |     BOLD = "bold"
7 |     ITALIC = "italic"
8 |     CODE = "code"
9 |     LINKS = "links"
10 |     IMAGES = "images"
11 | 
12 | 
13 | class TextNode:
14 |     def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
15 |         """
16 |         Args:
17 |             text: The text content of the node.
18 |             text_type: The type of text this node contains, which is a member of the TextType enum.
19 |             url: The URL of the link or image, if the text is a link. Default to None if nothing is passed in.
20 |         """
21 |         self.text = text
22 |         self.text_type = text_type
23 |         self.url = url
24 | 
25 |     def __eq__(self, other):
26 |         if not isinstance(other, TextNode):
27 |             raise ValueError("Must be TextNode instances")
28 |         return (
29 |             self.text == other.text
30 |             and self.text_type == other.text_type
31 |             and self.url == other.url
32 |         )
33 | 
34 |     def __repr__(self) -> str:
35 |         return f"TextNode(text={self.text!r}, text_type={self.text_type.value!r}, url={self.url!r})"
```

test.sh
```
1 | #!/bin/bash
2 | 
3 | python3 -m unittest discover "$@" -s src
```

