import os
from core import TextNode, TextType
from utils import sync_directories


def main():
    dummy_obj = TextNode("fañsdkljfa", TextType.BOLD, "https://nose")
    print(dummy_obj)


if __name__ == "__main__":
    main()

    # make sure "public" folder exist
    destination = "public"
    os.makedirs(os.path.join(os.path.dirname("src"), destination), exist_ok=True)

    sync_directories("static", destination)
