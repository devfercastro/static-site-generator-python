"""Just some file system function."""

import os
import shutil
from pathlib import Path


def invalid_path_error(context):
    raise ValueError(f"{context} must be a valid path")


def sync_directories(source: Path, destination: Path):
    """Syncronizes the contents of source directory to destination directory.

    Args:
        source: Path to the source directory to copy from
        destination: Path to the destination directory to copy to

    Raises:
        ValueError: If source or destination paths are invalid

    """

    def error_message(item):
        return f"{item} must be a valid path"

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
