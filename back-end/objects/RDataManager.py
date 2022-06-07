from genericpath import exists
import imp
import pickle
import sqlite3
import torchvision
import os.path as osp
import os
from utils.path_utils import get_paired_path, split_path, to_unix
import torch
from torchvision import transforms
from .RImageFolder import RImageFolder, RAnnotationFolder, REvalImageFolder, RTrainImageFolder
from PIL import Image
import torchvision.transforms.functional as transF


# The data interface
class RDataManager:

    SUPP_IMG_EXT = ['jpg', 'jpeg', 'png']

    def __init__(self, baseDir, datasetDir, dbPath, batch_size=32, shuffle=True, num_workers=8, image_size=32,
                 image_padding='short_side', class2label_mapping=None):

        # TODO: Support customized splits by taking a list of splits as argument
        # splits = ['train', 'test']
        self.data_root = datasetDir
        self.base_dir = baseDir
        self.db_path = dbPath
        self.batch_size = image_size
        self.shuffle = shuffle
        self.num_workers = num_workers
        self.image_size = image_size
        self.image_padding = image_padding
        self.class2label = class2label_mapping

        self._init_paths()
        self._init_db()
        self._init_transforms()
        self._init_data_records()

    
    def reload_influence_dict(self):
        if osp.exists(self.influence_file_path):
            print("Loading influence dictionary!")
            with open(self.influence_file_path, 'rb') as f:
                try:
                    # TODO: Check image_url -> image_path consistency here!
                    self.influenceBuffer = pickle.load(f)
                except Exception as e:
                    print("Influence function file not read because it is contaminated. \
                    Please delete it manually and start the server again!")

        else:
            print("No influence dictionary found!")

    def get_influence_dict(self):
        return self.influenceBuffer

    def _init_transforms(self):
        # Build transforms
        # TODO: Use different transforms according to image_padding variable
        # TODO: We need to double check to make sure that
        #       this is the only transform defined and used in Robustar.
        means = [0.485, 0.456, 0.406]
        stds = [0.229, 0.224, 0.225]
        self.transforms = transforms.Compose([
            SquarePad(self.image_padding),
            transforms.Resize((self.image_size, self.image_size)),
            transforms.ToTensor(),
            transforms.Normalize(means, stds)
        ])

    def _init_db(self):
        if osp.exists(self.db_path):
            print("DB already existed. Skipping initialization.")
            # TODO: May need to check for concurrency issues.
            self.db_conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.db_cursor = self.db_conn.cursor() 
            return

        print("DB file not found. Initializing db...")
        from utils.db import get_init_schema_str
        self.db_conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.db_cursor = self.db_conn.cursor() 
        self.db_cursor.executescript(get_init_schema_str())

        # Iterate through folders to construct database

        self.db_conn.commit()
        

    def _init_paths(self):
        self.test_root = to_unix(osp.join(self.data_root, "test"))
        self.train_root = to_unix(osp.join(self.data_root, 'train'))
        self.paired_root = to_unix(osp.join(self.data_root, 'paired'))
        self.validation_root = to_unix(osp.join(self.data_root, 'validation'))
        self.visualize_root = to_unix(osp.join(self.base_dir, 'visualize_images'))
        self.influence_root = to_unix(osp.join(self.base_dir, 'influence_images'))
        self.proposed_annotation_root = to_unix(osp.join(self.base_dir, 'proposed'))
        self.influence_file_path = to_unix(osp.join(self.influence_root, 'influence_images.pkl'))

    def _init_data_records(self):
        self.testset: REvalImageFolder = REvalImageFolder(self.test_root, 'test', self.db_conn, transform=self.transforms)
        self.trainset: RTrainImageFolder = RTrainImageFolder(self.train_root, 'train', self.db_conn, transform=self.transforms)
        if not os.path.exists(self.validation_root):
            self.validationset: REvalImageFolder = self.testset
        else:
            self.validationset: REvalImageFolder = REvalImageFolder(self.validation_root, 'validation', self.db_conn, transform=self.transforms)

        self.testloader = torch.utils.data.DataLoader(
            self.testset, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers)
        self.trainloader = torch.utils.data.DataLoader(
            self.trainset, batch_size=self.batch_size, shuffle=self.shuffle, num_workers=self.num_workers)
        self.validationloader = torch.utils.data.DataLoader(
            self.validationset, batch_size=self.batch_size, shuffle=False, num_workers=self.num_workers)

        self._init_folders()

        self.datasetFileBuffer = {}
        self.predictBuffer = {}
        self.influenceBuffer = {}

        self.proposedAnnotationBuffer = set() # saves (train image id)

        self.proposedset: RAnnotationFolder = RAnnotationFolder(self.proposed_annotation_root, self.train_root, 
                    split='proposed', db_conn=self.db_conn, transform=self.transforms) 
        ## TODO: Commented this line out for now, because if the user changed the training set, 
        ## The cache will be wrong, and the user has to manually delete the annotated folder, which
        ## is not nice. Add this back when we have the option to quickly clean all cache folders.
        # self.get_proposed_list()

        self.reload_influence_dict()
        # self.pairedset = torchvision.datasets.ImageFolder(self.paired_root, transform=self.transforms)
        self.pairedset: RAnnotationFolder = RAnnotationFolder(self.paired_root, self.train_root, 
                    split='annotated', db_conn=self.db_conn, transform=self.transforms)
        # self.pairedloader = torch.utils.data.DataLoader(
            # self.pairedloader, batch_size=batch_size, shuffle=False, num_workers=num_workers)

        self.split_dict = {
            'train': self.trainset,
            'validation': self.validationset,
            'test': self.testset,
            'annotated': self.pairedset,
            'proposed': self.proposedset
        }


    def _init_folders(self):
        for root in [self.visualize_root, self.influence_root, self.proposed_annotation_root]:
            os.makedirs(root, exist_ok=True)

        if not osp.exists(self.paired_root) or not os.listdir(self.paired_root):
            self._init_paired_folder()
        if not osp.exists(self.proposed_annotation_root) or not os.listdir(self.proposed_annotation_root):
            self._init_proposed_folder()
            
    def _init_paired_folder(self):
        # Initializes paired folder. Ignores files that already exists
        self._init_mirror_dir(self.train_root, self.trainset, self.paired_root)

    def _init_proposed_folder(self):
        # Initializes paired folder. Ignores files that already exists
        self._init_mirror_dir(self.train_root, self.trainset, self.proposed_annotation_root)

    def _init_mirror_dir(self, src_root, dataset, dst_root):
        if not osp.exists(dst_root):
            os.mkdir(dst_root)

        for img_path, label in dataset.samples:
            mirrored_img_path = get_paired_path(img_path, src_root, dst_root)

            if osp.exists(mirrored_img_path): # Ignore existing images
                continue

            folder_path, _ = split_path(mirrored_img_path)
            os.makedirs(folder_path, exist_ok=True)

            with open(mirrored_img_path, 'wb') as f:
                pass

    def _pull_item(self, index, buffer):
        if index >= len(buffer):
            return None
        return buffer[index]

    def get_db_conn(self):
        return self.db_conn

    def get_db_cursor(self):
        return self.db_cursor

# Return a square image
class SquarePad:
    image_padding = 'constant'

    def __init__(self, image_padding):
        self.image_padding = image_padding

    def __call__(self, image):
        # Reference: https://discuss.pytorch.org/t/how-to-resize-and-pad-in-a-torchvision-transforms-compose/71850/10
        if self.image_padding == 'none':
            return image
        elif self.image_padding == 'short_side':
            # Calculate the size of paddings
            max_size = max(image.size)
            pad_left, pad_top = [(max_size - size) // 2 for size in image.size]
            pad_right, pad_bottom = [max_size - (size + pad) for size, pad in zip(image.size, [pad_left, pad_top])]
            padding = (pad_left, pad_top, pad_right, pad_bottom)
            return transF.pad(image, padding, 0, 'constant')

        # TODO: Support more padding modes. E.g. pad both sides to given image size 
        else:
            raise NotImplementedError