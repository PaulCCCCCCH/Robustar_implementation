from utils.path_utils import get_paired_path, split_path, to_unix
from utils.image_utils import create_empty_paired_image
from torchvision.datasets import DatasetFolder, ImageFolder
from typing import Any, Callable, cast, Dict, List, Optional, Tuple
from PIL import Image
from io import BytesIO
from sqlite3.dbapi2 import Connection
from utils.db_ops import *
from collections import OrderedDict
import os
from os import path as osp

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

def get_slice(arr, start ,end):
    if start is None and end is None:
        return arr
    if end is None:
        return arr[start:]
    if start is None:
        return arr[:end]
    return arr[start:end]



SPLIT_TABLE_MAP = {
    'train': 'train_set',
    'validation': 'val_set',
    'test': 'test_set',
    'annotated': 'paired_set',
    'proposed': 'proposed'
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
    CLS_NONE = 0
    CLS_CORRECT = 0
    CLS_INCORRECT = 0 

    def __init__(
            self,
            root: str,
            split: str,
            db_conn: Connection,
            transform: Optional[Callable] = None,
            target_transform: Optional[Callable] = None,
            loader: Callable[[str], Any] = default_loader,
            is_valid_file: Optional[Callable[[str], bool]] = None,
            force_reindex: bool = False
    ):

        super(ImageFolder, self).__init__(root, loader, IMG_EXTENSIONS if is_valid_file is None else None,
                                          transform=transform,
                                          target_transform=target_transform,
                                          is_valid_file=is_valid_file)

        # Change all paths to unix
        for i in range(len(self.samples)):
            self.samples[i] = to_unix(self.samples[i])

        self.root = root
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
            values = [(path, self.CLS_NONE) for path, _ in self.imgs]
        else:
            # Do not re-index for other splits
            return
        
        db_insert_many(db_conn, self.table_name, keys, values)
        db_conn.commit()


    def get_image_list(self, start=None, end=None):
        return get_slice(self.samples, start, end)


class REvalImageFolder(RImageFolder):
    """
        An extended version of RImageFolder that supports the following:
        - Separate buffers for correctly and incorrectly classified samples
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
            force_reindex: bool = False
    ):

        super(REvalImageFolder, self).__init__(root, split, db_conn, 
                transform=transform, 
                target_transform=target_transform,
                loader=loader,
                is_valid_file=is_valid_file,
                force_reindex=force_reindex
        )

        self.buffer_correct = []
        self.buffer_incorrect = []
        self._init_records()

    def add_records(self, paths: List[str], correct: bool):
        buffer = self.buffer_correct if correct else self.buffer_incorrect

        paths = [to_unix(path) for path in paths]

        # 1. update db with the result
        db_update_many_by_paths(self.db_conn, self.table_name, paths, ('classified',), [correct for _ in paths])

        # 2. update buffer
        buffer.extend(paths)

        # 3. commit
        self.db_conn.commit()


    def add_record(self, path: str, correct: bool): 
        self.add_records[[to_unix(path)], correct]

    def get_record(self, correct: bool, start=None, end=None):
        buffer = self.buffer_correct if correct else self.buffer_incorrect
        return get_slice(buffer, start, end)
    
    def _init_records(self):
        for path, classified in db_select_all(self.db_conn, self.table_name):
            path = to_unix(path)
            if classified == self.CLS_CORRECT:
                self.buffer_correct.append(path)
            elif classified == self.CLS_INCORRECT:
                self.buffer_incorrect.append(path)



class RAnnotationFolder(RImageFolder):
    """
        An extended version of RImageFolder that supports the following:
        - O(1) Image lookup 
        - O(1) Image deletion
        - O(1) Image append

    """

    def __init__(
            self,
            root: str,
            train_root: str,
            split: str,
            db_conn: Connection,
            transform: Optional[Callable] = None,
            target_transform: Optional[Callable] = None,
            loader: Callable[[str], Any] = default_loader,
            is_valid_file: Optional[Callable[[str], bool]] = None,
    ):

        self.root = root
        self.train_root = train_root

        if not osp.exists(root) or not os.listdir(root):
            self._init_root_dir()
            

        super(RAnnotationFolder, self).__init__(root, split, db_conn, 
                transform=transform, 
                target_transform=target_transform,
                loader=loader,
                is_valid_file=is_valid_file,
        )

        # Do not use these from original ImageFolder, because random deletion will mess them up
        del self.imgs
        del self.samples 

        # init buffers
        self._init_buffers()

        # Read from database to memory
        for paired_path, train_path in db_select_all(self.db_conn, self.table_name):
            paired_path, train_path = to_unix(paired_path), to_unix(train_path)
            self._train2paired[train_path] = paired_path
            self._paired2train[paired_path] = train_path


    def remove_image(self, path):
        path = to_unix(path)
        # 1. delete the paired image in database...
        db_delete_by_path(self.db_conn, self.table_name, path)

        # 2. create an empty image placeholder
        os.remove(path) 
        create_empty_paired_image(path)

        # 3. update buffers
        train_path = self._paired2train[path]
        del self._train2paired[train_path]
        del self._paired2train[path]

        # 4. commit
        self.db_conn.commit()


    def clear_images(self):
        # 1. delete all paired images in database...
        db_delete_all(self.db_conn, self.table_name)

        # 2. create new paired folder
        os.remove(self.root) 
        self._init_root_dir()

        # 3. empty the buffers
        self._init_buffers()

        # 4. commit
        self.db_conn.commit()


    def add_image(self, train_path, image_data, image_height, image_width):
        train_path = to_unix(train_path)
        paired_path = get_paired_path(train_path, self.train_root, self.root)

        # 1. insert new paired path to db
        db_insert(self.db_conn, self.table_name, ("path", "train_path"), (paired_path, train_path)) 

        # 2. dump the image file to disk
        self._dump_image(paired_path, image_data, image_height, image_width)

        # 3. update buffers
        self._train2paired[train_path] = paired_path
        self._paired2train[paired_path] = train_path

        # 4. commit
        self.db_conn.commit()

    def get_paired_by_train(self, train_path):
        train_path = to_unix(train_path)
        if train_path in self._train2paired:
            return self._train2paired[train_path]
        return None

    def get_paired_path_by_train(self, train_path):
        train_path = to_unix(train_path)
        return get_paired_path(train_path, self.train_root, self.root)

    def get_image_list(self, start=None, end=None):
        # TODO: This has huge overhead.
        # Expect this function to be O(end-start), but here it's O(N) where N is the total number of annotated samples.
        key_list = list(self._paired2train.keys())
        return get_slice(key_list, start, end)


    def _dump_image(self, dump_path, image_data, image_height, image_width):
        with Image.open(BytesIO(image_data)) as img:
        
            to_save = img.resize((image_width, image_height))
            # to_save = to_save.convert('RGB') # in case image comming from canvas is RGBA
            to_save.save(dump_path, format='png')


    def _init_buffers(self):
        self._train2paired = OrderedDict()
        self._paired2train = OrderedDict()


    def _init_root_dir(self):
        if not osp.exists(self.root):
            os.mkdir(self.root)

        for img_path, _ in self.samples:
            mirrored_img_path = get_paired_path(img_path, self.train_root, self.root)

            if osp.exists(mirrored_img_path): # Ignore existing images
                continue

            folder_path, _ = split_path(mirrored_img_path)
            os.makedirs(folder_path, exist_ok=True)

            create_empty_paired_image(mirrored_img_path)