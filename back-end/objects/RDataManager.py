import collections
from flask import Flask
import pickle
import os.path as osp
import os
from pathlib import Path
from utils.path_utils import get_paired_path, split_path, to_unix
from torchvision import transforms
from flask_sqlalchemy import SQLAlchemy
from .RImageFolder import (
    RAnnotationFolder,
    REvalImageFolder,
    RTrainImageFolder,
    db_is_all_tables_empty,
)
import torchvision.transforms.functional as transF


# The data interface
class RDataManager:
    SUPP_IMG_EXT = ["jpg", "jpeg", "png"]

    def __init__(
        self,
        baseDir: str,
        dataset_dir: str,
        db_conn: SQLAlchemy,
        app: Flask,
        image_size=32,
        image_padding="short_side",
        class2label_mapping=None,
    ):
        # TODO: Support customized splits by taking a list of splits as argument
        # splits = ['train', 'test']
        self.data_root = dataset_dir
        self.base_dir = baseDir
        self.db_conn = db_conn
        self.image_size = image_size
        self.image_padding = image_padding
        self.class2label = class2label_mapping
        self.app = app

        self._init_paths()
        self._init_transforms()

        with app.app_context():
            self._init_data_records()

    def reload_influence_dict(self):
        if osp.exists(self.influence_file_path):
            print("Loading influence dictionary!")
            with open(self.influence_file_path, "rb") as f:
                try:
                    # TODO: Check image_url -> image_path consistency here!
                    self.influence_buffer = pickle.load(f)
                except Exception as e:
                    print(
                        "Influence function file not read because it is contaminated. \
                    Please delete it manually and start the server again!"
                    )

        else:
            print("No influence dictionary found!")

    def get_influence_dict(self):
        return self.influence_buffer

    def _init_transforms(self):
        # Build transforms
        # TODO: Use different transforms according to image_padding variable
        # TODO: We need to double check to make sure that
        #       this is the only transform defined and used in Robustar.
        means = [0.485, 0.456, 0.406]
        stds = [0.229, 0.224, 0.225]
        self.transforms = transforms.Compose(
            [
                SquarePad(self.image_padding),
                transforms.Resize((self.image_size, self.image_size)),
                transforms.ToTensor(),
                transforms.Normalize(means, stds),
            ]
        )

    def _init_paths(self):
        self.test_root = to_unix(osp.join(self.data_root, "test"))
        self.train_root = to_unix(osp.join(self.data_root, "train"))
        self.paired_root = to_unix(osp.join(self.data_root, "paired"))
        self.validation_root = to_unix(osp.join(self.data_root, "validation"))
        self.visualize_root = to_unix(osp.join(self.base_dir, "visualize_images"))
        self.influence_root = to_unix(osp.join(self.base_dir, "influence_images"))
        self.proposed_annotation_root = to_unix(osp.join(self.base_dir, "proposed"))
        self.influence_file_path = to_unix(
            osp.join(self.influence_root, "influence_images.pkl")
        )
        self.influence_log_path = to_unix(osp.join(self.influence_root, "logs"))

    def _init_data_records(self):
        # Check if we should recreate all db tables:
        should_reindex = db_is_all_tables_empty(self.db_conn)
        if should_reindex:
            print("Re-populating database with latest file system state")
        else:
            print("DB already exists. Not populating data.")

        self.testset: REvalImageFolder = REvalImageFolder(
            self.test_root,
            "test",
            self.db_conn,
            transform=self.transforms,
            should_reindex=should_reindex,
        )
        self.trainset: RTrainImageFolder = RTrainImageFolder(
            self.train_root,
            "train",
            self.db_conn,
            transform=self.transforms,
            should_reindex=should_reindex,
        )
        if not os.path.exists(self.validation_root):
            self.validationset: REvalImageFolder = self.testset
            self.validation_root = self.test_root
        else:
            self.validationset: REvalImageFolder = REvalImageFolder(
                self.validation_root,
                "validation",
                self.db_conn,
                transform=self.transforms,
                should_reindex=should_reindex,
            )

        self._init_folders()

        self.dataset_file_queue = collections.deque()
        self.dataset_file_queue_len = 1000
        self.dataset_file_buffer = {}

        self.influence_buffer = {}

        self.proposed_annotation_buffer = set()  # saves (train image id)

        self.proposedset: RAnnotationFolder = RAnnotationFolder(
            self.proposed_annotation_root,
            self.train_root,
            split="proposed",
            db_conn=self.db_conn,
            transform=self.transforms,
            should_reindex=should_reindex,
        )
        ## TODO: Commented this line out for now, because if the user changed the training set,
        ## The cache will be wrong, and the user has to manually delete the annotated folder, which
        ## is not nice. Add this back when we have the option to quickly clean all cache folders.
        # self.get_proposed_list()

        self.reload_influence_dict()
        # self.pairedset = torchvision.datasets.ImageFolder(self.paired_root, transform=self.transforms)
        self.pairedset: RAnnotationFolder = RAnnotationFolder(
            self.paired_root,
            self.train_root,
            split="annotated",
            db_conn=self.db_conn,
            transform=self.transforms,
            should_reindex=should_reindex,
        )

        self.split_dict = {
            "train": self.trainset,
            "validation": self.validationset,
            "test": self.testset,
            "annotated": self.pairedset,
            "proposed": self.proposedset,
        }

    def _init_folders(self):
        for root in [
            self.visualize_root,
            self.influence_root,
            self.proposed_annotation_root,
        ]:
            os.makedirs(root, exist_ok=True)

        if not osp.exists(self.paired_root) or not os.listdir(self.paired_root):
            self._init_paired_folder()
        if not osp.exists(self.proposed_annotation_root) or not os.listdir(
            self.proposed_annotation_root
        ):
            self._init_proposed_folder()

    def _init_paired_folder(self):
        # Initializes paired folder. Ignores files that already exists
        self._init_mirror_dir(self.train_root, self.trainset, self.paired_root)

    def _init_proposed_folder(self):
        # Initializes paired folder. Ignores files that already exists
        self._init_mirror_dir(
            self.train_root, self.trainset, self.proposed_annotation_root
        )

    def _init_mirror_dir(self, src_root, dataset, dst_root):
        if not osp.exists(dst_root):
            os.mkdir(dst_root)

        for img_path, label in dataset.samples:
            mirrored_img_path = get_paired_path(img_path, src_root, dst_root)

            if osp.exists(mirrored_img_path):  # Ignore existing images
                continue

            folder_path, _ = split_path(mirrored_img_path)
            os.makedirs(folder_path, exist_ok=True)

            with open(mirrored_img_path, "wb") as f:
                pass

    def _pull_item(self, index, buffer):
        if index >= len(buffer):
            return None
        return buffer[index]

    def get_db_conn(self):
        return self.db_conn

    def dispose_db_engine(self):
        with self.app.app_context():
            self.db_conn.engine.dispose()


class SquarePad:
    """
    A transform that takes a PIL image and pad it into a square
    """

    image_padding = "constant"

    def __init__(self, image_padding):
        self.image_padding = image_padding

    def __call__(self, image):
        # Reference: https://discuss.pytorch.org/t/how-to-resize-and-pad-in-a-torchvision-transforms-compose/71850/10
        if self.image_padding == "none":
            # Does not pad
            return image
        elif self.image_padding == "short_side":
            # Calculate the size of paddings required to make a square
            max_size = max(image.size)
            pad_left, pad_top = [(max_size - size) // 2 for size in image.size]
            pad_right, pad_bottom = [
                max_size - (size + pad)
                for size, pad in zip(image.size, [pad_left, pad_top])
            ]
            padding = (pad_left, pad_top, pad_right, pad_bottom)
            return transF.pad(image, padding, 0, "constant")
        else:
            raise NotImplementedError
