import os
import shutil
from pathlib import Path

from markdown import extract_title, markdown_to_html_node


def invalid_path_error(context):
    raise ValueError(f"{context} must be a valid path")


def sync_directories(source: Path, destination: Path):
    """Cleans the destination then syncronizes the contents of source directory to destination directory.

    Args:
        source: Path to the source directory to copy from
        destination: Path to the destination directory to copy to

    Raises:
        ValueError: If source or destination paths are invalid

    """
    if not source.exists():
        invalid_path_error("source")

    if not destination.exists():
        invalid_path_error("destination")

    # clean the destination
    shutil.rmtree(destination)
    Path.mkdir(destination)

    def _copy_recursive(current_path: Path, copy_destination: Path):
        """Recursively copies directory contents while preserving structure.

        Args:
            current_path: Current directory path beign processed
            copy_destination: Target path for current directory

        """
        # create destination subdirectory
        Path.mkdir(copy_destination, exist_ok=True)

        for item in os.listdir(current_path):
            item_path = current_path / item

            # if file, just copy
            if item_path.is_file():
                shutil.copy(item_path, copy_destination)

            # if directory, update destination and recursively call the function
            else:
                new_destination = copy_destination / item
                _copy_recursive(item_path, new_destination)

    _copy_recursive(source, destination)


def generate_page(from_path: Path, template_path: Path, dest_path: Path):
    """Generate an HTML page from a markdown file using a template

    Args:
        from_path: The path of the markdown file
        template_path: The path of the HTML template file
        dest_path: The path where the generated HTML file will be

    Raises:
        ValueError: If from_path or template_path are invalid paths

    """
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    # check if path are valid
    if not from_path.exists():
        invalid_path_error("from_path")
    if not template_path.exists():
        invalid_path_error("template_path")
    # create `dest_path`'s parents if nedeed
    dest_path.parent.mkdir(parents=True, exist_ok=True)

    # read the markdown
    with open(from_path) as f:
        markdown = f.read()
    # read the template
    with open(template_path) as f:
        template = f.read()

    # extract the nodes from markdown
    html_nodes = markdown_to_html_node(markdown)
    # extract the title from markdown
    title = extract_title(markdown)
    # build html content
    html_content = "\n".join([node.to_html() for node in html_nodes])

    # replace placeholders
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_content)

    # write the new html file
    with open(dest_path, "w") as f:
        f.write(template)


def generate_page_recursive(
    dir_path_content: Path, template_path: Path, dest_dir_path: Path
):
    """Converts markdown files from a source directory to HTML using a template and puts them in a destination directory

    Args:
        dir_path_content (Path): The path to the source directory containing markdown files.
        template_path (Path): The path to the template file.
        dest_dir_path (Path): The path to the destination directory where the generated HTML files will be placed.

    Raises:
        ValueError: If the source directory does not exist.
        ValueError: If the destination directory does not exist.

    """
    # validate paths
    if not dir_path_content.exists():
        invalid_path_error("dir_path_content")
    if not dest_dir_path.exists():
        invalid_path_error("dest_dir_path")

    def _process_directory(current_path: Path, dest_path: Path):
        """Recursively converts markdown files to HTML

        Args:
            current_path (Path): The current path being processed.
            dest_path (Path): The destination path for the generated HTML files.
        """
        # Create the destination directory if it doesn't exist
        Path.mkdir(dest_path, exist_ok=True)

        # Process each item in the current directory
        for item in os.listdir(current_path):
            # Get the full path of the current item
            item_path = current_path / item

            # If is a file, process it
            if item_path.is_file():
                # Generated file name
                new_file = item_path.stem + ".html"
                generate_page(item_path, template_path, dest_path / new_file)
            # If is a directory, continue recursion
            elif item_path.is_dir():
                _process_directory(item_path, dest_path / item_path.name)

    _process_directory(dir_path_content, dest_dir_path)
