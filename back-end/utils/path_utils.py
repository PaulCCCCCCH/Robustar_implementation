from os.path import normpath as ospn
from os.path import join


def split_path(path):
    """
    Split path into folder path and filename.
    e.g. 'folder' -> None, 'folder'
         'path/to/file/filename.py' -> 'path/to/file', 'filename.py'

    args:
        path: The path to be split

    returns:
        folder_path
        filename
    """

    path_split = ospn(path).split('/')

    # Only one segment in the path, e.g. 'folder'
    if len(path_split) == 1:
        return None, path_split[0]


    # Otherwise, split 'path/to/file/filename.py' to 'path/to/file' and 'filename.py'
    folder_path = join(*path_split[:-1])
    filename = path_split[-1]
    return folder_path, filename