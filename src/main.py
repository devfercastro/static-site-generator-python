from helpers import copy_content
from textnode import TextNode, TextType


def main():
    dummy_obj = TextNode("fañsdkljfa", TextType.BOLD, "https://nose")
    print(dummy_obj)


if __name__ == "__main__":
    main()
    copy_content("static", "public")
