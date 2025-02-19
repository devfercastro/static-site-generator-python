import os
import shutil


def copy_content(source: str, destination: str):
    """
    Copies the all the contents from `source` to `destination` recursivelly

    Args:
        source: The source directory where to extract the contents
        destination: The destination where to put the extracted contents

    Raises:
        ValueError: If `source` or `destination` params are invalid paths
    """
    if not os.path.exists(source):
        raise ValueError("`source` must be a valid path")
    if not os.path.exists(destination):
        raise ValueError("`destination` must be a valid path")

    # clean the destination
    shutil.rmtree(destination)
    os.mkdir(destination)

    def copy_helper(current_path: str, copy_destination: str):
        """
        Helper function that recursivelly copy the contents of one directory to another

        Args:
            current_path: The current path to copy from
            copy_destination: The path to copy to
        """
        # add the subdir on the destination folder
        if not os.path.exists(copy_destination):
            os.mkdir(copy_destination)

        for item in os.listdir(current_path):
            fullpath = os.path.join(current_path, item)
            # if file, just copy
            if os.path.isfile(fullpath):
                shutil.copy(fullpath, copy_destination)
            # if directory, update destination and recursivelly call the function
            else:
                new_destination = os.path.join(copy_destination, item)
                copy_helper(fullpath, new_destination)

    copy_helper(source, destination)
