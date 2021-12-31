'''
Author: Chonghan Chen (paulcccccch@gmail.com)
-----
Last Modified: Tuesday, 7th December 2021 10:45:14 pm
Modified By: Chonghan Chen (paulcccccch@gmail.com)
-----
'''
from genericpath import exists
import pickle
import torchvision
import os.path as osp
import os
from utils.path_utils import get_paired_path, split_path
import torch
from torchvision import transforms
from PIL import Image
import torchvision.transforms.functional as transF


# The data interface
class RDataManager:

    def __init__(self, baseDir, datasetDir, batch_size=32, shuffle=True, num_workers=8, image_size=32,
                 image_padding='short_side'):
    # def __init__(self, datasetPath, image_size, image_padding):

        # TODO: Support customized splits by taking a list of splits as argument
        # splits = ['train', 'test']
        self.data_root = datasetDir
        self.base_dir = baseDir
        self.batch_size = image_size
        self.shuffle = shuffle
        self.num_workers = num_workers
        self.image_size = image_size
        self.image_padding = image_padding
        self.test_root = osp.join(datasetDir, "test").replace('\\', '/')
        self.train_root = osp.join(datasetDir, 'train').replace('\\', '/')
        self.paired_root = osp.join(datasetDir, 'paired').replace('\\', '/')
        self.validation_root = osp.join(datasetDir, 'validation').replace('\\', '/')
        self.visualize_root = osp.join(baseDir, 'visualize_images').replace('\\', '/')
        self.influence_root = osp.join(baseDir, 'influence_images').replace('\\', '/')
        self.influence_file_path = osp.join(self.influence_root, 'influence_images.pkl').replace('\\', '/')


        self.test_correct_root = osp.join(datasetDir, 'test_correct.txt').replace('\\', '/')
        self.test_incorrect_root = osp.join(datasetDir, 'test_incorrect.txt').replace('\\', '/')
        self.validation_correct_root = osp.join(datasetDir, 'validation_correct.txt').replace('\\', '/')
        self.validation_incorrect_root = osp.join(datasetDir, 'validation_incorrect.txt').replace('\\', '/')

        # Build transforms
        # TODO: Use different transforms according to image_padding variable
        # TODO: We need to double check to make sure that
        #       this is the only transform defined and used in Robustar.
        means = [0.485, 0.456, 0.406]
        stds = [0.229, 0.224, 0.225]
        self.transforms = transforms.Compose([
            SquarePad(image_padding),
            transforms.Resize((image_size)),
            transforms.ToTensor(),
            transforms.Normalize(means, stds)
        ])

        self.testset = torchvision.datasets.ImageFolder(self.test_root, transform=self.transforms)
        self.trainset = torchvision.datasets.ImageFolder(self.train_root, transform=self.transforms)
        if not os.path.exists(self.validation_root):
            self.validationset = self.testset
        else:
            self.validationset = torchvision.datasets.ImageFolder(self.validation_root)

        self.testloader = torch.utils.data.DataLoader(
            self.testset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
        self.trainloader = torch.utils.data.DataLoader(
            self.trainset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)
        self.validationloader = torch.utils.data.DataLoader(
            self.validationset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

        self._init_folders()

        self.datasetFileBuffer = {}
        self.predictBuffer = {}
        self.influenceBuffer = {}

        self.correctValidationBuffer = []
        self.incorrectValidationBuffer = []
        self.correctTestBuffer = []
        self.incorrectTestBuffer = []

        self.get_classify_validation_list()
        self.get_classify_test_list()

        self.reload_influence_dict()
        self.split_dict = {
            'train': self.trainset.samples,
            'validation': self.validationset.samples,
            'test': self.testset.samples,
            'validation_correct': self.correctValidationBuffer,
            'validation_incorrect': self.incorrectValidationBuffer,
            'test_correct': self.correctTestBuffer,
            'test_incorrect': self.incorrectTestBuffer
        }


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

    def _init_folders(self):
        if not osp.exists(self.paired_root) or not os.listdir(self.paired_root):
            self._init_paired_folder()
        self._init_visualize_root()

    def _init_influence_root(self):
        os.makedirs(self.influence_root, exist_ok=True)

    def _init_visualize_root(self):
        os.makedirs(self.visualize_root, exist_ok=True)

    def _init_paired_folder(self):
        # Initializes paired folder. Ignores files that already exists
        if not osp.exists(self.paired_root):
            os.mkdir(self.paired_root)

        for img_path, label in self.trainset.samples:
            paired_img_path = get_paired_path(img_path, self.train_root, self.paired_root)

            if osp.exists(paired_img_path):  # Ignore existing images
                continue

            folder_path, _ = split_path(paired_img_path)
            os.makedirs(folder_path, exist_ok=True)

            with open(paired_img_path, 'wb') as f:
                pickle.dump(None, f)

    def get_classify_validation_list(self):
        if not osp.exists(self.validation_correct_root):
            f = open(self.validation_correct_root, 'w')  # cannot use os.mknod because it's not supported by Windows
            f.close()
        else:
            with open(self.validation_correct_root, 'r') as f:
                for line in f:
                    self.correctValidationBuffer.append(int(line))

        if not osp.exists(self.validation_incorrect_root):
            f = open(self.validation_incorrect_root, 'w')
            f.close()
        else:
            with open(self.validation_incorrect_root, 'r') as f:
                for line in f:
                    self.incorrectValidationBuffer.append(int(line))

    def get_classify_test_list(self):
        if not osp.exists(self.test_correct_root):
            f = open(self.test_correct_root, 'w')
            f.close()
        else:
            with open(self.test_correct_root, 'r') as f:
                for line in f:
                    self.correctTestBuffer.append(int(line))

        if not osp.exists(self.test_incorrect_root):
            f = open(self.test_incorrect_root, 'w')
            f.close()
        else:
            with open(self.test_incorrect_root, 'r') as f:
                for line in f:
                    self.incorrectTestBuffer.append(int(line))

    def _pull_item(self, index, buffer):
        if index >= len(buffer):
            return None
        return buffer[index]

    def get_correct_validation(self, index):
        return self._pull_item(index, self.correctValidationBuffer)

    def get_incorrect_validation(self, index):
        return self._pull_item(index, self.incorrectValidationBuffer)

    def get_correct_test(self, index):
        return self._pull_item(index, self.correctTestBuffer)

    def get_incorrect_test(self, index):
        return self._pull_item(index, self.incorrectTestBuffer)



# Return a square image
class SquarePad:
    image_padding = 'constant'

    def __init__(self, image_padding):
        self.image_padding = image_padding

    def __call__(self, image):
        # Reference: https://discuss.pytorch.org/t/how-to-resize-and-pad-in-a-torchvision-transforms-compose/71850/10
        if self.image_padding =='none':
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
            raise NotImplemented

if __name__ == '__main__':

    # Test
    # dataManager = RDataManager('/Robustar2/dataset')
    # print(dataManager.trainset.imgs[0])
    # print(osp.exists('/Robustar2/x'))

    transforms = transforms.Compose([
        SquarePad('short_side'),
        transforms.Resize((600, 600)),
    ])

    img = Image.open('C:\\Users\\paulc\\Desktop\\temp.png')
    print(img.size)
    trans = transforms(img)
    trans.save('C:\\Users\\paulc\\Desktop\\temp_trans.png')

