'''
Author: Chonghan Chen (paulcccccch@gmail.com)
-----
Last Modified: Tuesday, 7th December 2021 10:45:14 pm
Modified By: Chonghan Chen (paulcccccch@gmail.com)
-----
'''
import pickle
import torchvision
import os.path as osp
import os
from utils.path_utils import get_paired_path, split_path



# The data interface
class RDataManager:

    def __init__(self, datasetPath):

        # TODO: Support customized splits by taking a list of splits as argument
        # splits = ['train', 'test']
        self.data_root = datasetPath
        self.test_root =osp.join(datasetPath, "test").replace('\\', '/')
        self.train_root = osp.join(datasetPath, 'train').replace('\\', '/')
        self.paired_root = osp.join(datasetPath, 'paired').replace('\\', '/')

        self.testset = torchvision.datasets.ImageFolder(self.test_root)
        self.trainset = torchvision.datasets.ImageFolder(self.train_root)

        if not osp.exists(self.paired_root) or not os.listdir(self.paired_root):
            self.init_paired_folder()

        self.datasetFileBuffer = {}
        self.predictBuffer = {}
        self.correctBuffer = {}
        self.mistakeBuffer = {}


    def init_paired_folder(self):
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