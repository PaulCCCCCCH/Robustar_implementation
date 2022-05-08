from utils.path_utils import get_paired_path, split_path, to_unix
from torchvision.datasets import DatasetFolder, ImageFolder
from typing import Any, Callable, cast, Dict, List, Optional, Tuple
from PIL import Image
from sqlite3.dbapi2 import Connection
from utils.db_ops import *

IMG_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.ppm', '.bmp', '.pgm', '.tif', '.tiff', '.webp')


# Helper functions copied from torchvision.datasets.folder
def pil_loader(path: str) -> Image.Image:
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, 'rb') as f:
        img = Image.open(f)
        return img.convert('RGB')


def accimage_loader(path: str) -> Any:
    try:
        import accimage
        return accimage.Image(path)
    except IOError:
        # Potentially a decoding problem, fall back to PIL.Image
        return pil_loader(path)


def default_loader(path: str) -> Any:
    from torchvision import get_image_backend
    if get_image_backend() == 'accimage':
        return accimage_loader(path)
    else:
        return pil_loader(path)

SPLIT_TABLE_MAP = {
    'train': 'train_set',
    'validation': 'val_set',
    'test': 'test_set',
    'paired': 'paired_set',
}



class RImageFolder(DatasetFolder):
    """
        An extended version of PyTorch's ImageFolder that connects to SQLite database on disk.
        

    Args:
        root (string): Root directory path.
        split: the split we are dealing with
        db_cursor: interface for db operation
        transform (callable, optional): A function/transform that  takes in an PIL image
            and returns a transformed version. E.g, ``transforms.RandomCrop``
        target_transform (callable, optional): A function/transform that takes in the
            target and transforms it.
        loader (callable, optional): A function to load an image given its path.
        is_valid_file (callable, optional): A function that takes path of an Image file
            and check if the file is a valid file (used to check of corrupt files)
        force_reindex: force the train, val and test sets to be re-indexed and written to db

     Attributes:
        classes (list): List of the class names sorted alphabetically.
        class_to_idx (dict): Dict with items (class_name, class_index).
        imgs (list): List of (image path, class_index) tuples
    """

    def __init__(
            self,
            root: str,
            split: str,
            db_conn: Connection,
            transform: Optional[Callable] = None,
            target_transform: Optional[Callable] = None,
            loader: Callable[[str], Any] = default_loader,
            is_valid_file: Optional[Callable[[str], bool]] = None,
            force_reindex = False
    ):

        super(ImageFolder, self).__init__(root, loader, IMG_EXTENSIONS if is_valid_file is None else None,
                                          transform=transform,
                                          target_transform=target_transform,
                                          is_valid_file=is_valid_file)

        self.split = split
        self.db_conn = db_conn
        self.imgs = self.samples
        self.table_name = SPLIT_TABLE_MAP[split]

        # Return if no need to rebuild the index;
        if not force_reindex and db_count_all(db_conn, SPLIT_TABLE_MAP[split]) == 0:
            return

        if split == "train":
            keys = ("path", "paired_path")
            values = [(path, None) for path, _ in self.imgs]
        elif split == "validation" or "test":
            keys = ("path", "classified")
            values = [(path, 0) for path, _ in self.imgs]
        else:
            # Do not re-index for other splits
            return
        
        db_insert_many(db_conn, self.table_name, keys, values)
        db_conn.commit()
                    

class RPairedImageFolder(RImageFolder):
    """
        An extended version of PyTorch's ImageFolder that supports the following:
        - O(1) Image lookup with image id
        - O(1) Image deletion
        - O(1) Image insertion

    """

    def remove_image(self, path):
        db_delete_by_path(self.db_conn, self.table_name, path)
        self.db_conn.commit()


    def clear_images(self):
        db_delete_all(self.db_conn, self.table_name)
        self.db_conn.commit()


    def add_image(self, train_path):
        paired_path = get_paired_path(train_path) 

        db_insert(self.db_conn, self.table_name, ("path", "train_path"), (paired_path, train_path)) 
        self.db_conn.commit()

