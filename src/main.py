import argparse
from pathlib import Path

from utils import generate_page_recursive, sync_directories


def main():
    parser = argparse.ArgumentParser(description="Static Site Generator")
    parser.add_argument(
        "--basepath",
        type=str,
        nargs="?",
        default="/",
        help="Base path for relative links (default: '/')",
    )
    parser.add_argument(
        "--source",
        type=str,
        default="content",
        help="Path to markdown content (default: 'content')",
    )
    parser.add_argument(
        "--template",
        type=str,
        default="template.html",
        help="Path to template file (default: 'template.html')",
    )
    parser.add_argument(
        "--static",
        type=str,
        default="static",
        help="Path to static files directory (default: 'static')",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="docs",
        help="Path to output directory (default: 'docs')",
    )

    args = parser.parse_args()

    basepath = args.basepath
    source = Path(args.source)
    template = Path(args.template)
    statics = Path(args.static)
    output = Path(args.output)

    # Ensure the "public" directory exists.
    # Create the directory along with any necessary parent directories.
    output.mkdir(parents=True, exist_ok=True)

    # cleans the destination, then syncs the contents
    sync_directories(statics, output)

    generate_page_recursive(source, template, output, basepath)


if __name__ == "__main__":
    main()
