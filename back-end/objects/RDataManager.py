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



# The data interface
class RDataManager:

    def __init__(self, baseDir, datasetDir, batch_size=32, shuffle=True, num_workers=8, image_size=32, image_padding='none'):

        # TODO: Support customized splits by taking a list of splits as argument
        # splits = ['train', 'test']
        self.data_root = datasetDir
        self.base_dir = baseDir
        self.image_size = image_size
        self.image_padding = image_padding
        self.test_root =osp.join(datasetDir, "test")
        self.train_root = osp.join(datasetDir, 'train')
        self.paired_root = osp.join(datasetDir, 'paired')
        self.visualize_root = osp.join(baseDir, 'visualize_images')
        self.influence_root = osp.join(baseDir, 'influence_images')
        self.influence_file_path = osp.join(self.influence_root, 'influence_images.pkl')

        # Build transforms
        # TODO: Use different transforms according to image_padding variable
        # TODO: We need to double check to make sure that
        #       this is the only transform defined and used in Robustar.
        means = [0.485, 0.456, 0.406]
        stds = [0.229, 0.224, 0.225]
        self.transforms = transforms.Compose([
            transforms.Resize(image_size),
            transforms.CenterCrop(image_size),
            transforms.ToTensor(),
            transforms.Normalize(means, stds)
        ])
        
        self.testset = torchvision.datasets.ImageFolder(self.test_root, transform=self.transforms)
        self.trainset = torchvision.datasets.ImageFolder(self.train_root, transform=self.transforms)

        self.testloader = torch.utils.data.DataLoader(
            self.testset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
        self.trainloader = torch.utils.data.DataLoader(
            self.trainset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)

        self._init_folders()

        self.datasetFileBuffer = {}
        self.predictBuffer = {}
        self.correctBuffer = {}
        self.mistakeBuffer = {}
        self.influenceBuffer = {}

        self.reload_influence_dict()

    def reload_influence_dict(self):
        if osp.exists(self.influence_file_path):
            print("Loading influence dictionary!")
            self.influenceBuffer = pickle.load(self.influence_file_path)
        else:
            print("No influence dictionary found!")

    def get_influence_dict(self):
        return self.influenceBuffer

    def _init_folders(self):
        if not osp.exists(self.paired_root) or not os.listdir(self.paired_root):
            self._init_paired_folder()
        self._init_visualize_root()

    def _init_influence_root(self):
        os.makedirs(self.influence_root, exists_ok=True)

    def _init_visualize_root(self):
        os.makedirs(self.visualize_root, exist_ok=True)

    def _init_paired_folder(self):
        # Initializes paired folder. Ignores files that already exists
        if not osp.exists(self.paired_root):
            os.mkdir(self.paired_root)

        for img_path, label in self.trainset.samples:
            paired_img_path = get_paired_path(img_path, self.train_root, self.paired_root)

            if osp.exists(paired_img_path): # Ignore existing images
                continue
                
            folder_path, _ = split_path(paired_img_path)
            os.makedirs(folder_path, exist_ok=True)

            with open(paired_img_path, 'wb') as f:
                pickle.dump(None, f)

    

if __name__ == '__main__':

    # Test
    dataManager = RDataManager('/Robustar2/dataset')
    # print(dataManager.trainset.imgs[0])
    print(osp.exists('/Robustar2/x'))
