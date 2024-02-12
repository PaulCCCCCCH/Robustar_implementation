from utils.path_utils import (
    get_paired_path,
    split_path,
    to_unix,
    create_empty_paired_image,
)
from torchvision.datasets import DatasetFolder, ImageFolder
from typing import Any, Callable, cast, Dict, List, Optional, Tuple, Union
from PIL import Image
from io import BytesIO
from collections import OrderedDict
from flask_sqlalchemy import SQLAlchemy
from database.model import *
import os
from os import path as osp

IMG_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".ppm",
    ".bmp",
    ".pgm",
    ".tif",
    ".tiff",
    ".webp",
)


# Helper functions copied from torchvision.datasets.folder
def pil_loader(path: str) -> Image.Image:
    # open path as file to avoid ResourceWarning (https://github.com/python-pillow/Pillow/issues/835)
    with open(path, "rb") as f:
        img = Image.open(f)
        return img.convert("RGB")


def accimage_loader(path: str) -> Any:
    try:
        import accimage

        return accimage.Image(path)
    except IOError:
        # Potentially a decoding problem, fall back to PIL.Image
        return pil_loader(path)


def default_loader(path: str) -> Any:
    from torchvision import get_image_backend

    if get_image_backend() == "accimage":
        return accimage_loader(path)
    else:
        return pil_loader(path)


def get_slice(arr, start, end):
    if start is None and end is None:
        return arr
    if end is None:
        return arr[start:]
    if start is None:
        return arr[:end]
    return arr[start:end]


def db_is_all_tables_empty(db_conn: SQLAlchemy):
    for table in db_conn.Model.metadata.tables.values():
        row_count = (
            db_conn.session.query(db_conn.func.count()).select_from(table).scalar()
        )
        if row_count > 0:
            return False

    return True


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
        should_reindex: shall we re-create all metadata for the database to reflect the latest
            images in the file system

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
        db_conn: SQLAlchemy,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None,
        loader: Callable[[str], Any] = default_loader,
        is_valid_file: Optional[Callable[[str], bool]] = None,
        should_reindex: bool = False,
        class2label: dict[str, str] = None,
    ):
        super(RImageFolder, self).__init__(
            root,
            loader,
            IMG_EXTENSIONS if is_valid_file is None else None,
            transform=transform,
            target_transform=target_transform,
            is_valid_file=is_valid_file,
        )

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
        self.class2label = class2label
        self.imgs = self.samples

        # Return if no need to rebuild the index;
        if should_reindex:
            self._populate_db()

    def _populate_db(self):
        # with self.db_conn.session.begin():
        if "train" in self.split:
            print(
                "Populating the db table train_set_image for split {}".format(
                    self.split
                )
            )
            images = [
                TrainSetImage(path=path, paired_path=None, label=label)
                for path, label in self.imgs
            ]
        elif "validation" in self.split:
            print(
                "Populating the db table val_set_image for split {}".format(self.split)
            )
            images = [ValSetImage(path=path, label=label) for path, label in self.imgs]
        elif "test" in self.split:
            print(
                "Populating the db table test_set_image for split {}".format(self.split)
            )
            images = [TestSetImage(path=path, label=label) for path, label in self.imgs]
        else:  # Do not re-index for other splits
            print(f"No database table to be populated for split {self.split}")
            return
        self.db_conn.session.add_all(images)
        self.db_conn.session.commit()

    def get_image_list(self, start=None, end=None):
        if start is not None and len(self.samples) <= start:
            raise ValueError("Out of upper-bound")
        return [p[0] for p in get_slice(self.samples, start, end)]

    def readify_classes(self):
        self.classes = [self.class2label.get(c, c) for c in self.classes]
        self.class_to_idx = {c: idx for idx, c in enumerate(self.classes)}


class RTrainImageFolder(RImageFolder):
    def __init__(
        self,
        root: str,
        split: str,
        db_conn: SQLAlchemy,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None,
        loader: Callable[[str], Any] = default_loader,
        is_valid_file: Optional[Callable[[str], bool]] = None,
        should_reindex: bool = False,
        class2label: dict[str, str] = None,
    ):
        super(RTrainImageFolder, self).__init__(
            root,
            split,
            db_conn,
            transform=transform,
            target_transform=target_transform,
            loader=loader,
            is_valid_file=is_valid_file,
            should_reindex=should_reindex,
            class2label=class2label,
        )

        self._init_next_imgs()
        self._init_buffer()
        self._populate_buffer()

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
        for train_set_image in TrainSetImage.query.all():
            path = to_unix(train_set_image.path)
            if train_set_image.paired_path is not None:
                self.train2paired[path] = train_set_image.paired_path


class REvalImageFolder(RImageFolder):
    """
    An extended version of RImageFolder that supports the following:
    - Separate buffers for correctly and incorrectly classified samples
    """

    def __init__(
        self,
        root: str,
        split: str,
        db_conn: SQLAlchemy,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None,
        loader: Callable[[str], Any] = default_loader,
        is_valid_file: Optional[Callable[[str], bool]] = None,
        should_reindex: bool = False,
        class2label: dict[str, str] = None,
    ):
        super(REvalImageFolder, self).__init__(
            root,
            split,
            db_conn,
            transform=transform,
            target_transform=target_transform,
            loader=loader,
            is_valid_file=is_valid_file,
            should_reindex=should_reindex,
            class2label=class2label,
        )

        self.buffer_correct = []
        self.buffer_incorrect = []
        self._populate_buffers()
        self._init_next_records()

    def post_records(
        self,
        correct_records: List[Tuple[str, int]],
        incorrect_records: List[Tuple[str, int]],
    ):
        correct_paths = [to_unix(record[0]) for record in correct_records]
        incorrect_paths = [to_unix(record[0]) for record in incorrect_records]

        # 1. update db with the result
        # TODO: get model ID here
        for path in correct_paths:
            result = EvalResults(model_id=0, img_path=path, result=self.CLS_CORRECT)
            self.db_conn.session.merge(result)

        for path in incorrect_paths:
            result = EvalResults(model_id=0, img_path=path, result=self.CLS_INCORRECT)
            self.db_conn.session.merge(result)

        # 3. update buffer
        self.buffer_correct = correct_records
        self.buffer_incorrect = incorrect_records

        # 4. update next record datastructure
        self._init_next_records()

        # 5. commit
        self.db_conn.session.commit()

    def get_next_record(self, path, correct: bool):
        next_record = self.next_correct if correct else self.next_incorrect
        return next_record.get(path, None)

    def _init_next_records(self):
        self.next_imgs = dict()
        for (img_path, _), (next_img_path, _) in zip(self.imgs, self.imgs[1:]):
            self.next_imgs[img_path] = next_img_path

        self.next_correct = dict()
        for (img_path, _), (next_img_path, _) in zip(
            self.buffer_correct, self.buffer_correct[1:]
        ):
            self.next_correct[img_path] = next_img_path

        self.next_incorrect = dict()
        for (img_path, _), (next_img_path, _) in zip(
            self.buffer_incorrect, self.buffer_incorrect[1:]
        ):
            self.next_incorrect[img_path] = next_img_path

    def get_record(self, correct: bool, start=None, end=None):
        buffer = self.buffer_correct if correct else self.buffer_incorrect
        if start and len(buffer) <= start:
            raise ValueError("Out of upper-bound")
        return [p[0] for p in get_slice(buffer, start, end)]

    def _populate_buffers(self):
        if "validation" in self.split:
            table_to_query = ValSetImage
        elif "test" in self.split:
            table_to_query = TestSetImage
        else:
            raise ValueError(f"Split {self.split} is not supported!")

        correct_results = (
            self.db_conn.session.query(table_to_query)
            .join(EvalResults, EvalResults.img_path == table_to_query.path)
            .filter(EvalResults.result == 0)
            .all()
        )
        self.buffer_correct = [(res.path, res.label) for res in correct_results]

        incorrect_results = (
            self.db_conn.session.query(table_to_query.path)
            .join(EvalResults, EvalResults.img_path == table_to_query.path)
            .filter(EvalResults.result == 1)
            .all()
        )
        self.buffer_incorrect = [(res.path, res.label) for res in incorrect_results]


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
        db_conn: SQLAlchemy,
        transform: Optional[Callable] = None,
        target_transform: Optional[Callable] = None,
        loader: Callable[[str], Any] = default_loader,
        is_valid_file: Optional[Callable[[str], bool]] = None,
        should_reindex: bool = False,
        class2label: dict[str, str] = None,
    ):
        self.root = root
        self.train_root = train_root

        if not osp.exists(root) or not os.listdir(root):
            self._init_root_dir()

        super(RAnnotationFolder, self).__init__(
            root,
            split,
            db_conn,
            transform=transform,
            target_transform=target_transform,
            loader=loader,
            is_valid_file=is_valid_file,
            should_reindex=should_reindex,
            class2label=class2label,
        )

        # Do not use these from original ImageFolder, because random deletion will mess them up
        del self.imgs
        del self.samples

        if "annotated" in self.split:
            self.db_model = PairedSetImage
        elif "proposed" in self.split:
            self.db_model = ProposedImage
        else:
            raise NotImplemented

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
        self.db_conn.session.query(self.db_model).filter(
            self.db_model.path == path
        ).delete()

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
        self.db_conn.session.commit()
        return True

    def clear_images(self):
        # 1. delete all paired images in database...
        self.db_conn.session.query(self.db_model).delete()

        # 2. create new paired folder
        # No need to explicitly do this, just let paired images be there.
        # If records in db are removed, they are not going to be used anyway.

        # 3. empty the buffers
        self._init_buffers()
        self.next_records = dict()
        self.prev_records = dict()

        # 4. commit
        self.db_conn.session.commit()

    def save_annotated_image(
        self,
        train_path,
        trainset: RTrainImageFolder,
        image_data: Union[Image.Image, bytes],
        image_height=None,
        image_width=None,
    ):
        train_path = to_unix(train_path)
        paired_path = get_paired_path(train_path, self.train_root, self.root)

        # 1. insert new paired path to db if image not already annotated
        # if train_path not in self._train2paired:
        new_paired_image = self.db_model(path=paired_path, train_path=train_path)
        self.db_conn.session.merge(new_paired_image)

        # 2. update corresponding training image
        if self.db_model == PairedSetImage:
            train_image_to_update = TrainSetImage.query.filter_by(path=train_path)
            train_image_to_update.paired_path = paired_path

            trainset.train2paired[train_path] = paired_path

        # 3. dump the image file to disk
        if isinstance(image_data, Image.Image):  # If image_data is PIL Image
            image_data.save(paired_path, format="png")
        else:  # If image_data is an array of bytes
            if image_height is None or image_width is None:
                raise ValueError("must specify image height and width")
            self._dump_image_data(paired_path, image_data, image_height, image_width)

        # 4. update buffers
        self._train2paired[train_path] = paired_path
        self._paired2train[paired_path] = train_path

        # 5. update next record datastructures
        if self.last_record:
            self.next_records[self.last_record] = paired_path
            self.prev_records[paired_path] = self.last_record
        self.last_record = paired_path

        # 6. commit
        self.db_conn.session.commit()

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
            to_save.save(dump_path, format="png")

    def _init_buffers(self):
        self._train2paired = OrderedDict()
        self._paired2train = OrderedDict()

    def _init_root_dir(self):
        if not osp.exists(self.root):
            os.mkdir(self.root)

        for img_path, _ in self.samples:
            mirrored_img_path = get_paired_path(img_path, self.train_root, self.root)

            if osp.exists(mirrored_img_path):  # Ignore existing images
                continue

            folder_path, _ = split_path(mirrored_img_path)
            os.makedirs(folder_path, exist_ok=True)

            create_empty_paired_image(mirrored_img_path)

    def _populate_buffers(self):
        for paired_data in self.db_model.query.all():
            paired_path, train_path = to_unix(paired_data.path), to_unix(
                paired_data.train_path
            )
            self._train2paired[train_path] = paired_path
            self._paired2train[paired_path] = train_path

    def _init_next_records(self):
        paired_imgs = self.get_image_list()
        for img_path, next_img_path in zip(paired_imgs, paired_imgs[1:]):
            self.next_records[img_path] = next_img_path
            self.prev_records[next_img_path] = img_path
        if paired_imgs:
            self.last_record = paired_imgs[-1]
