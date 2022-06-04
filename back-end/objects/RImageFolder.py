from utils.path_utils import get_paired_path, split_path, to_unix, create_empty_paired_image
from torchvision.datasets import DatasetFolder, ImageFolder
from typing import Any, Callable, cast, Dict, List, Optional, Tuple, Union
import PIL
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
    CLS_CORRECT = 1
    CLS_INCORRECT = 2

    def __init__(
            self,
            root: str,
            split: str,
            db_conn: Connection,
            transform: Optional[Callable] = None,
            target_transform: Optional[Callable] = None,
            loader: Callable[[str], Any] = default_loader,
            is_valid_file: Optional[Callable[[str], bool]] = None,
            force_reindex: bool = False,
            class2label: dict[str, str] = None 
    ):

        super(RImageFolder, self).__init__(root, loader, IMG_EXTENSIONS if is_valid_file is None else None,
                                          transform=transform,
                                          target_transform=target_transform,
                                          is_valid_file=is_valid_file)


        # Change all paths to unix
        for i in range(len(self.samples)):
            tup = self.samples[i]
            self.samples[i] = (to_unix(tup[0]), tup[1])

        # If class2label mapping is provided, change all labels
        if class2label is not None:
            self.readify_classes()

        self.root = root
        self.split = split
        self.db_conn = db_conn
        self.table_name = SPLIT_TABLE_MAP[split]
        self.class2label = class2label
        self.imgs = self.samples

        # Return if no need to rebuild the index;
        if not force_reindex and db_count_all(db_conn, SPLIT_TABLE_MAP[split]) > 0:
            return

        if split == "train":
            keys = ("path", "paired_path")
            values = [(path, None) for path, _ in self.imgs]
        elif split == "validation" or split == "test":
            keys = ("path", "classified")
            values = [(path, self.CLS_NONE) for path, _ in self.imgs]
        else: # Do not re-index for other splits
            print('Not populating the db table {}'.format(self.table_name))
            return

        print("Populating the db table {} for split {}".format(self.table_name, split))  
        db_insert_many(db_conn, self.table_name, keys, values)
        db_conn.commit()


    def get_image_list(self, start=None, end=None):
        return [p[0] for p in get_slice(self.samples, start, end)]


    def readify_classes(self):
        self.classes = [self.class2label.get(c, c) for c in self.classes]
        self.class_to_idx = {c: idx for idx, c in enumerate(self.classes)}


class RTrainImageFolder(RImageFolder):

    def __init__(
            self,
            root: str,
            split: str,
            db_conn: Connection,
            transform: Optional[Callable] = None,
            target_transform: Optional[Callable] = None,
            loader: Callable[[str], Any] = default_loader,
            is_valid_file: Optional[Callable[[str], bool]] = None,
            force_reindex: bool = False,
            class2label: dict[str, str] = None 
    ):

        super(RTrainImageFolder, self).__init__(root, split, db_conn, 
                transform=transform, 
                target_transform=target_transform,
                loader=loader,
                is_valid_file=is_valid_file,
                force_reindex=force_reindex,
                class2label=class2label
        )


        self._init_next_imgs()
        self._init_buffer()
        self._populate_buffer()
        

    def update_paired_data(self, train_paths: List[str], paired_paths: List[str]):
        train_paths = [to_unix(train_path) for train_path in train_paths]
        paired_paths = [to_unix(paired_path) for paired_path in paired_paths]

        # 1. update database
        db_update_many_by_paths(self.db_conn, self.table_name, train_paths, 
            keys=("paired_path", ), values_list=[(paired_path,) for paired_path in paired_paths])

        # 2. update buffer
        for train_path, paired_path in zip(train_paths, paired_paths):
            self.train2paired[train_path] = paired_path

        # 3. commit
        self.db_conn.commit()

    def get_paired_from_train(self, train_path):
        train_path = to_unix(train_path)
        if train_path in self.train2paired:
            return self.train2paired[train_path]
        return None

    def get_next_image(self, image_path):
        return self.next_imgs.get(image_path, None)


    def _init_next_imgs(self):
        self.next_imgs = dict()
        for (img_path, _), (next_img_path, _) in zip(self.imgs, self.imgs[1:]):
            self.next_imgs[img_path] = next_img_path 


    def _init_buffer(self):
        self.train2paired = dict()

    def _populate_buffer(self):
        for path, paired_path in db_select_all(self.db_conn, self.table_name):
            path = to_unix(path)
            if paired_path is not None:
                self.train2paired[path] = paired_path



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
            force_reindex: bool = False,
            class2label: dict[str, str] = None 
    ):

        super(REvalImageFolder, self).__init__(root, split, db_conn, 
                transform=transform, 
                target_transform=target_transform,
                loader=loader,
                is_valid_file=is_valid_file,
                force_reindex=force_reindex,
                class2label=class2label
        )

        self.buffer_correct = []
        self.buffer_incorrect = []
        self._populate_buffers()
        self._init_next_records()

    def add_records(self, records: List[Tuple[str, int]], correct: bool):
        buffer = self.buffer_correct if correct else self.buffer_incorrect
        next_record = self.next_correct if correct else self.next_incorrect

        paths = [to_unix(record[0]) for record in records]

        # 1. update db with the result
        db_update_many_by_paths(self.db_conn, self.table_name, paths, ('classified',), [correct for _ in paths])

        # 2. update buffer
        buffer.extend(records)
        
        # 3. update next record datastructure
        for (img_path, _), (next_img_path, _) in zip([buffer[-1]] + records, records):
            next_record[img_path] = next_img_path

        # 4. commit
        self.db_conn.commit()

    def add_record(self, pair: Tuple[str, int], correct: bool): 
        self.add_records([(to_unix(pair[0]), pair[1])], correct)


    def get_next_record(self, path, correct: bool):
        next_record = self.next_correct if correct else self.next_incorrect
        return next_record.get(path, None)


    def _init_next_records(self):
        self.next_imgs = dict()
        for (img_path, _), (next_img_path, _) in zip(self.imgs, self.imgs[1:]):
            self.next_imgs[img_path] = next_img_path 

        self.next_correct = dict()
        for (img_path, _), (next_img_path, _) in zip(self.buffer_correct, self.buffer_correct[1:]):
            self.next_correct[img_path] = next_img_path 
       
        self.next_incorrect = dict()
        for (img_path, _), (next_img_path, _) in zip(self.buffer_incorrect, self.buffer_incorrect[1:]):
            self.next_incorrect[img_path] = next_img_path 

    def get_record(self, correct: bool, start=None, end=None):
        buffer = self.buffer_correct if correct else self.buffer_incorrect
        return [p[0] for p in get_slice(buffer, start, end)]
    
    def _populate_buffers(self):
        db_data = db_select_all(self.db_conn, self.table_name)
        # database and sample data must contain same number of images
        assert(len(db_data) == len(self.samples)) 

        for (imgpath, label), (path, classified) in zip(self.imgs, db_data):
            # paths must be in the same order, i.e., folder and database 
            # must be consistent
            assert(imgpath == path) 

            path = to_unix(path)
            if classified == self.CLS_CORRECT:
                self.buffer_correct.append((path, label))
            elif classified == self.CLS_INCORRECT:
                self.buffer_incorrect.append((path, label))



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
            class2label: dict[str, str] = None 
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
                class2label=class2label
        )

        # Do not use these from original ImageFolder, because random deletion will mess them up
        del self.imgs
        del self.samples 

        # init buffers
        self._init_buffers()

        # Read from database to memory
        self._populate_buffers()

        # Initializa next record datastructure
        self.last_record = None
        self.next_records = dict()
        self.prev_records = dict()
        self._init_next_records()
        


    def remove_image(self, path):
        path = to_unix(path)
        # 1. delete the paired image in database...
        db_delete_by_path(self.db_conn, self.table_name, path)

        # 2. create an empty image placeholder
        os.remove(path) 
        create_empty_paired_image(path)

        # 3. update next records datastructures
        prev_record = self.prev_records.get(path, None)
        next_record = self.next_records.get(path, None)
        if next_record:
            self.prev_records[next_record] = prev_record
        if prev_record:
            self.next_records[prev_record] = next_record

        # 4. update buffers
        train_path = self._paired2train[path]
        del self._train2paired[train_path]
        del self._paired2train[path]

        # 5. commit
        self.db_conn.commit()
        return True


    def clear_images(self):
        # 1. delete all paired images in database...
        db_delete_all(self.db_conn, self.table_name)

        # 2. create new paired folder
        os.remove(self.root) 
        self._init_root_dir()

        # 3. empty the buffers
        self._init_buffers()
        self.next_records = dict()
        self.prev_records = dict()

        # 4. commit
        self.db_conn.commit()


    def save_annotated_image(self, train_path, image_data: Union[Image.Image, bytes], image_height=None, image_width=None):
        train_path = to_unix(train_path)
        paired_path = get_paired_path(train_path, self.train_root, self.root)

        # 1. insert new paired path to db if image not already annotated
        if train_path not in self._train2paired:
            db_insert(self.db_conn, self.table_name, ("path", "train_path"), (paired_path, train_path)) 

        # 2. dump the image file to disk
        if isinstance(image_data, Image.Image): # If image_data is PIL Image
            image_data.save(paired_path, format='png')
        else: # If image_data is an array of bytes
            if image_height is None or image_width is None: raise ValueError("must specify image height and width")
            self._dump_image_data(paired_path, image_data, image_height, image_width)

        # 3. update buffers
        self._train2paired[train_path] = paired_path
        self._paired2train[paired_path] = train_path

        # 4. update next record datastructures
        if self.last_record:
            self.next_records[self.last_record] = paired_path
            self.prev_records[paired_path] = self.last_record
        self.last_record = paired_path

        # 5. commit
        self.db_conn.commit()

    def get_paired_by_train(self, train_path):
        """
        Get paired path of the train path if paired image exists. Otherwise, return None.
        """
        train_path = to_unix(train_path)
        if train_path in self._train2paired:
            return self._train2paired[train_path]
        return None

    def get_train_by_paired(self, paired_path):
        """
        Get train path of the paired path if paired image exists. Otherwise, return None.
        """
        paired_path = to_unix(paired_path)
        if paired_path in self._paired2train:
            return self._paired2train[paired_path]
        return None

    def convert_paired_path_to_train(self, paired_path):
        """
        Get train path of the paired path, no matter whether the paired image exists or not.
        """
        paired_path = to_unix(paired_path)
        return get_paired_path(paired_path, self.root, self.train_root)


    def convert_train_path_to_paired(self, train_path):
        """
        Get paired path of the train path, no matter whether the paired image exists or not.
        """
        train_path = to_unix(train_path)
        return get_paired_path(train_path, self.train_root, self.root)

    def get_image_list(self, start=None, end=None):
        # TODO: This has huge overhead.
        # Expect this function to be O(end-start), but here it's O(N) where N is the total number of annotated samples.
        key_list = list(self._paired2train.keys())
        return get_slice(key_list, start, end)

    def is_annotated(self, train_path):
        """
        Return if the given training image is annotated or not
        """
        return train_path in self._train2paired

    def get_next_image(self, paired_path):
        paired_path = to_unix(paired_path)
        return self.next_records.get(paired_path, None)


    def _dump_image_data(self, dump_path, image_data, image_height, image_width):
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
        

    def _populate_buffers(self):
        for paired_path, train_path in db_select_all(self.db_conn, self.table_name):
            paired_path, train_path = to_unix(paired_path), to_unix(train_path)
            self._train2paired[train_path] = paired_path
            self._paired2train[paired_path] = train_path

    def _init_next_records(self):
        paired_imgs = self.get_image_list()
        for img_path, next_img_path in zip(paired_imgs, paired_imgs[1:]):
            self.next_records[img_path] = next_img_path
            self.prev_records[next_img_path] = img_path 
        if paired_imgs:
            self.last_record = paired_imgs[-1]