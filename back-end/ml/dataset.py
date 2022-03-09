import numpy as np
import torch
import torchvision.datasets as dset
import torchvision.transforms as transforms
from PIL import Image
from torch.utils.data import Dataset

from objects.RModelWrapper import RModelWrapper

# Chonghan FIXME: There seems to be a bug with my environment. Added this for now.
# https://github.com/explosion/spaCy/issues/7664
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


###########################################


class DataSet(Dataset):

    def __init__(self, data_folder, image_size, transforms, classes_path=None):
        self.data_folder = data_folder
        self.image_size = image_size
        self.dataset = dset.ImageFolder(root=data_folder, transform=transforms)

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        return self.dataset[idx]


class PairedDataset(DataSet):
    mixture_methods = ['pure_black', 'noise', 'noise_weak', 'noise_minor', 'random_pure', 'hstrips', 'vstrips']

    def __init__(self, data_folder, paired_data_folder, image_size, transforms, classes_path, mode):
        super(PairedDataset, self).__init__(data_folder, image_size, transforms, classes_path)
        print("********************")
        print(paired_data_folder)
        print("********************")
        self.paired_data_folder = paired_data_folder
        self.paired_dataset = dset.ImageFolder(root=paired_data_folder, loader=paired_loader, transform=transforms)
        self.mode = mode

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        paired_data = self.__get_paired_data(idx)
        return self.dataset[idx], paired_data

    def __get_paired_data(self, idx):
        paired_image, _ = self.paired_dataset[idx]  # p: (data, label).
        if paired_image is None:  # this image has no paired data, just return the original image
            return self.dataset[idx]

        return self.__get_aug_image(self.dataset[idx][0], paired_image), self.dataset[idx][1]

    def __get_aug_image(self, image, paired_image):
        """
        Args:
            image: the original image tensor of shape (size, size, 3)
            paired_image: the paired image tensor (size, size, 3)
        Returns:
            a new image of shape (size, size, 3), with background filled according to `mode`
        """

        # FIXME: not completed
        # user_edit =

        # new_image = image.clone()  # clone the image to avoid pollution
        # new_image[user_edit == 1] = 0  # the area marked by the user is the background and should be cleared
        #
        # if self.mode == 'mixture':
        #     mode_idx = np.random.randint(len(self.MIXTURE_METHODS))
        #     mode = self.mixture_methods[mode_idx]
        # else:
        #     mode = self.mode
        #
        # bg_data = get_aug_background(user_edit, mode)  # (N, 1, 28, 28, 3)
        # new_image = new_image + bg_data
        #
        # return new_image


def paired_loader(path):
    if os.path.getsize(path):
        # print(os.path.getsize(path))
        img = Image.open(path)
        return img
    return None


def get_aug_background(bg_data, mode):
    """
    Args:
        bg_data: user-edit pytorch tensor of shape (3, size, size)
        mode: how to augment the data
    Returns:
        the augmented background
    """

    img_size = list(bg_data.shape)

    if mode == 'pure_black':
        bg_data = torch.zeros(size=img_size)

    elif mode == 'noise':
        bg_data = torch.rand(size=img_size) * bg_data
        # bg_data = bg_data.to(torch.uint8)

    elif mode == 'noise_weak':
        bg_data = (0.5 * (torch.rand(size=img_size)) + 0.25) * bg_data
        # bg_data = bg_data.to(torch.uint8)

    elif mode == 'noise_minor':
        bg_data = (0.1 * (torch.rand(size=img_size)) + 0.45) * bg_data
        # bg_data = bg_data.to(torch.uint8)

    elif mode == 'random_pure':
        colour_map = torch.rand(size=(3, 1, 1))
        bg_data = bg_data * colour_map  # (3, 28, 28)

    elif mode == 'hstrips':
        colour_map = torch.rand(size=(3, 1, 1))
        strips = torch.zeros_like(bg_data)  # (3, size, size)

        indices = np.arange(bg_data.shape[1])
        indices = np.where(indices % 5 < 2)
        strips[:, indices, :] = 1
        bg_data = strips * bg_data  # element-wise product, shape unchanged
        bg_data = bg_data * colour_map

    elif mode == 'vstrips':
        colour_map = torch.rand(size=(3, 1, 1))
        strips = torch.zeros_like(bg_data)  # (3, size, size)

        indices = np.arange(bg_data.shape[2])
        indices = np.where(indices % 5 < 2)
        strips[:, :, indices] = 1
        bg_data = strips * bg_data  # element-wise product, shape unchanged
        bg_data = bg_data * colour_map

    else:
        raise NotImplementedError

    return bg_data