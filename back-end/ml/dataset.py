from torchvision.datasets import ImageFolder
import torch
from PIL import Image
from torch.utils.data import Dataset
import os
import numpy as np
from PIL import Image

# Chonghan FIXME: There seems to be a bug with my environment. Added this for now.
# https://github.com/explosion/spaCy/issues/7664
import os

os.environ["KMP_DUPLICATE_LIB_OK"] = "True"


class ImageFolderNoTransform(ImageFolder):
    """
    An ImageFolder object that does not apply transforms
    Reference:
    https://github.com/pytorch/vision/blob/4ec38d496db69833eb0a6f144ebbd6f751cd3912/torchvision/datasets/folder.py#L129

    This is necessary because transforms have to be applied after the creation of
    augmented data.
    """

    def __getitem__(self, index):
        """
        Args:
            index (int): Index
        Returns:
            tuple: (sample, target) where target is class_index of the target class.
        """
        path, target = self.samples[index]
        sample = self.loader(path)
        # if self.transform is not None:
        #     sample = self.transform(sample)
        if self.target_transform is not None:
            target = self.target_transform(target)

        return sample, target


class DataSet(Dataset):
    def __init__(self, data_folder, image_size, transforms, classes_path=None):
        self.data_folder = data_folder
        self.image_size = image_size
        self.dataset = ImageFolderNoTransform(root=data_folder)
        self.transforms = transforms

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        img, label = self.dataset[idx]
        return self.transforms(img), label


class PairedDataset(DataSet):
    """
    Require paired data to be in png format.
    """

    mixture_methods = [
        "pure_black",
        "noise",
        "noise_weak",
        "noise_minor",
        "random_pure",
        "hstrips",
        "vstrips",
    ]

    def __init__(
        self,
        data_folder,
        paired_data_folder,
        image_size,
        transforms,
        classes_path,
        mode,
        user_edit_buffering=False,
    ):
        super(PairedDataset, self).__init__(
            data_folder, image_size, transforms, classes_path
        )

        loader = (
            self.paired_loader_with_buffer
            if user_edit_buffering
            else self.paired_loader
        )
        self.user_edit_dataset = ImageFolderNoTransform(
            root=paired_data_folder, loader=loader
        )
        self.paired_data_folder = paired_data_folder
        self.mode = mode
        self.user_edit_buffer = {}

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        img, label = self.dataset[idx]
        aug_img, _ = self.__get_paired_data(idx)
        return (self.transforms(img), label), (self.transforms(aug_img), label)

    def __get_paired_data(self, idx):
        data, label = self.dataset[idx]

        user_edit_arr, _ = self.user_edit_dataset[idx]  # p: (data, label).
        if (
            user_edit_arr is None
        ):  # this image has no paired data, just return the original image
            return data, label
        aug_img = self.__get_aug_image(self.dataset[idx][0], user_edit_arr)
        return aug_img, label

    def paired_loader(self, path):
        if os.path.getsize(path) == 0:
            return None

        img = Image.open(path)
        imgarr = np.array(img)
        user_edit = 1 * np.equal(imgarr, [255] * imgarr.shape[2]).all(axis=2)
        return torch.tensor(user_edit)

    def paired_loader_with_buffer(self, path):
        if path in self.user_edit_buffer:  # Return if already buffered
            return self.user_edit_buffer[path]

        user_edit = self.paired_loader(path)  # Find user edit region
        self.user_edit_buffer[path] = user_edit
        return user_edit

    def __get_aug_image(self, image, user_edit):
        """
        Args:
            image: PIL.Image of original training dataset
            user_edit: numpy array of shape (size, size)
            mode: how to augment the data
        Returns:
            a new PIL.Image with background filled according to `mode`
        """
        user_edit = np.stack(
            [user_edit, user_edit, user_edit], axis=2
        )  # Expand to RGB repr of shape (size, size, 3)

        imgarr = np.array(image)  # (size, size, 3)
        imgarr[
            user_edit == 1
        ] = 0  # the area marked by the user is the background and should be cleared

        if self.mode == "mixture":
            mode_idx = np.random.randint(len(self.MIXTURE_METHODS))
            mode = self.mixture_methods[mode_idx]
        else:
            mode = self.mode

        bg_data = get_aug_background(user_edit, mode)  # (size, size, 3)
        imgarr = imgarr + bg_data

        return Image.fromarray(imgarr)


def get_aug_background(bg_data, mode):
    """
    Args:
        bg_data: user-edit pytorch tensor of shape (size, size, 3)
        mode: how to augment the data
    Returns:
        the augmented background
    """

    img_size = list(bg_data.shape)

    if mode == "pure_black":
        bg_data = np.zeros(shape=img_size)

    elif mode == "noise":
        bg_data = np.random.randint(0, 256, img_size) * bg_data

    elif mode == "noise_weak":
        bg_data = np.random.randint(64, 192, img_size) * bg_data

    elif mode == "noise_minor":
        bg_data = np.random.randint(96, 160, img_size) * bg_data

    elif mode == "random_pure":
        colour_map = np.random.randint(0, 256, size=(1, 1, 3))
        bg_data = bg_data * colour_map  # (size, size, 3)

    elif mode == "hstrips":
        colour_map = np.random.randint(0, 256, size=(1, 1, 3))
        strips = np.zeros_like(bg_data)  # (size, size, 3)

        indices = np.arange(bg_data.shape[0])
        indices = np.where(indices % 5 < 2)
        strips[indices, :, :] = 1
        bg_data = strips * bg_data  # element-wise product, shape unchanged
        bg_data = bg_data * colour_map

    elif mode == "vstrips":
        colour_map = np.random.randint(0, 256, size=(1, 1, 3))
        strips = np.zeros_like(bg_data)  # (size, size, 3)

        indices = np.arange(bg_data.shape[1])
        indices = np.where(indices % 5 < 2)
        strips[:, indices, :] = 1
        bg_data = strips * bg_data  # element-wise product, shape unchanged
        bg_data = bg_data * colour_map

    else:
        raise NotImplementedError

    return bg_data.astype(np.uint8)
