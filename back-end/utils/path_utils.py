from os.path import normpath, join
import re

def create_empty_paired_image(path):
    with open(path, 'wb') as f:
        pass


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

    path_split = normpath(path).replace('\\', '/').split('/')

    # Only one segment in the path, e.g. 'folder'
    if len(path_split) == 1:
        return None, path_split[0]

    # Otherwise, split 'path/to/file/filename.py' to 'path/to/file' and 'filename.py'
    folder_path = '/'.join(path_split[:-1])
    filename = path_split[-1]
    return folder_path, filename


def replace_folder(path, new_folder):
    """
    Change the last folder in path to new_folder
    e.g. 'path/to/folder', folder2 -> 'path/to/folder2'
         'folder', 'folder2' -> 'folder2'

    args:
        path: The path to be replaced

    returns:
        new folder path
    """

    dirs = normpath(path).replace('\\', '/').split('/')
    dirs[-1] = new_folder
    return '/'.join(dirs)


def get_paired_path(img_path, prev_root, paired_root):
    """
    Find the mirrored path of the given image path.
    prev_root has to be part of img_path
    >>> get_paired_path('/Robustar2/dataset/train/1/2134.jpg', '/Robustar2/dataset/train', '/Robustar2/dataset/paired')
    '/Robustar2/dataset/paired/1/2134.jpg'

    args:
        img_path: path to the image
        origin_root: 
        paired_root: mirrored image root

    returns:
        new image path
    """
    return re.sub(prev_root, paired_root, img_path)


def to_unix(path):
    return join('/', path.replace('\\', '/'))



if __name__ == '__main__':
    assert replace_folder('/Robustar2/dataset/train', 'paired') == '/Robustar2/dataset/paired'
    assert get_paired_path('/Robustar2/dataset/train/1/2134.jpg',
                           '/Robustar2/dataset/train',
                           '/Robustar2/dataset/paired'
                           ) == '/Robustar2/dataset/paired/1/2134.jpg'

    print(split_path('/Robustar2/dataset/train/0/2134.jpg'))
    assert split_path('/Robustar2/dataset/train/0/2134.jpg') == ('/Robustar2/dataset/train/0', '2134.jpg')
    print('passed')
