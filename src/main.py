"""Just the main file."""

from pathlib import Path

from core import TextNode, TextType
from utils import sync_directories, generate_page


def main():
    """Execute the program.

    This function creates a dummy TextNode object and synchronizes
    the contents of the 'static' directory to the 'public' directory.
    """
    dummy_obj = TextNode("fañsdkljfa", TextType.BOLD, "https://nose")
    print(dummy_obj)


if __name__ == "__main__":
    main()

    destination = Path("public")
    # Ensure the "public" directory exists.
    # Create the directory along with any necessary parent directories.
    destination.mkdir(parents=True, exist_ok=True)

    sync_directories(Path("static"), destination)

    markdown = Path("content/index.md")
    template = Path("template.html")
    output = Path("index.html")

    generate_page(markdown, template, output)
