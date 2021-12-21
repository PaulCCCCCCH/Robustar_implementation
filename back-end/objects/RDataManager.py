'''
Author: Chonghan Chen (paulcccccch@gmail.com)
-----
Last Modified: Wednesday, 17th November 2021 12:52:14 pm
Modified By: Chonghan Chen (paulcccccch@gmail.com)
-----
'''

import torchvision
import os.path as osp
from torchvision import transforms
from PIL import Image
import torchvision.transforms.functional as tf


# The data interface
class RDataManager:

    def __init__(self, datasetPath, image_size, image_padding):

        self.testset = torchvision.datasets.ImageFolder(root=osp.join(datasetPath, "test"))
        self.trainset = torchvision.datasets.ImageFolder(root=osp.join(datasetPath, "train"))

        self.datasetFileBuffer = {}
        self.predictBuffer = {}
        self.correctBuffer = {}
        self.mistakeBuffer = {}

        self.image_size = image_size
        # self.image_padding = image_padding
        self.SquarePad.image_padding = image_padding

        # Define the size transformer according to the given image_size and image_padding
        self.size_transformer = transforms.Compose({
            self.SquarePad(),
            transforms.Resize((self.image_size, self.image_size))
        })

    # Return a square image
    class SquarePad:
        image_padding = 'constant'

        def __call__(self, image):
            # Reference: https://discuss.pytorch.org/t/how-to-resize-and-pad-in-a-torchvision-transforms-compose/71850/10

            # Calculate the size of paddings
            max_size = max(image.size)
            pad_left, pad_top = [(max_size - size) // 2 for size in image.size]
            pad_right, pad_bottom = [max_size - (size + pad) for size, pad in zip(image.size, [pad_left, pad_top])]
            padding = (pad_left, pad_top, pad_right, pad_bottom)

            # Pad the image according to the mode
            if (self.image_padding == 'constant'):
                return tf.pad(image, padding, 0, 'constant')
            elif (self.image_padding == 'edge'):
                return tf.pad(image, padding, padding_mode='edge')
            elif (self.image_padding == 'reflect'):
                return tf.pad(image, padding, padding_mode='reflect')
            elif (self.image_padding == 'symmetric'):
                return tf.pad(image, padding, padding_mode='symmetric')




if __name__ == '__main__':

    # Test
    dataManager = RDataManager('/Robustar2/dataset', 224, 'constant')
    # print(dataManager.trainset.samples[0])
    #
    # img = Image.open(dataManager.trainset.samples[0][0])

    img = Image.open('C:\\Users\\Lamb\\Desktop\\Leon\\Identification\\test.jpg')

    img = dataManager.size_transformer(img)
    img.save('C:\\Users\\Lamb\\Desktop\\test.jpg')
    # img.show()