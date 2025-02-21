import os
import shutil


def sync_directories(source: str, destination: str):
    """
    Syncronizes the contents of source directory to destination directory

    Args:
        source: Path to the source directory to copy from
        destination: Path to the destination directory to copy to

    Raises:
        ValueError: If source or destination paths are invalid
    """
    if not os.path.exists(source):
        raise ValueError("`source` must be a valid path")
    if not os.path.exists(destination):
        raise ValueError("`destination` must be a valid path")

    # clean the destination
    shutil.rmtree(destination)
    os.mkdir(destination)

    def _copy_recursive(current_path: str, copy_destination: str):
        """
        Recursively copies directory contents while preserving structure

        Args:
            current_path: Current directory path beign processed
            copy_destination: Target path for current directory
        """
        # create destination subdirectory
        os.mkdir(copy_destination)

        for item in os.listdir(current_path):
            item_path = os.path.join(current_path, item)

            # if file, just copy
            if os.path.isfile(item_path):
                shutil.copy(item_path, copy_destination)

            # if directory, update destination and recursively call the function
            else:
                new_destination = os.path.join(copy_destination, item)
                _copy_recursive(item_path, new_destination)

    _copy_recursive(source, destination)
