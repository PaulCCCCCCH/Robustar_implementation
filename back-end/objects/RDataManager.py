'''
Author: Chonghan Chen (paulcccccch@gmail.com)
-----
Last Modified: Wednesday, 17th November 2021 12:52:14 pm
Modified By: Chonghan Chen (paulcccccch@gmail.com)
-----
'''

import torchvision
import os.path as osp



# The data interface
class RDataManager:

    def __init__(self, datasetPath):

        self.testset = torchvision.datasets.ImageFolder(root=osp.join(datasetPath, "test"))
        self.trainset = torchvision.datasets.ImageFolder(root=osp.join(datasetPath, "train"))

        self.datasetFileBuffer = {}
        self.predictBuffer = {}
        self.correctBuffer = {}
        self.mistakeBuffer = {}


if __name__ == '__main__':
    # Test
    dataManager = RDataManager('/Robustar2/dataset')
    print(dataManager.trainset.samples[0])