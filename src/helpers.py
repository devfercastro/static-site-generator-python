import os
import shutil


def copy_content(source: str, destination: str):
    if not os.path.exists(source):
        raise ValueError("`source` must be a valid path")
    if not os.path.exists(destination):
        raise ValueError("`destination` must be a valid path")

    shutil.rmtree(destination)
    os.mkdir(destination)

    def copy_helper(current_path: str, copy_destination: str):
        if not os.path.exists(copy_destination):
            os.mkdir(copy_destination)

        for item in os.listdir(current_path):
            fullpath = os.path.join(current_path, item)
            if os.path.isfile(fullpath):
                shutil.copy(fullpath, copy_destination)
            else:
                new_destination = os.path.join(copy_destination, item)
                copy_helper(fullpath, new_destination)

    copy_helper(source, destination)
