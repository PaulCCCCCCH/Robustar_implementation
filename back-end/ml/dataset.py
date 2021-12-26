import torchvision.transforms as transforms
import torchvision.datasets as dset
import torch
from torch.utils.data import Dataset
import os
import numpy as np

# Chonghan FIXME: There seems to be a bug with my environment. Added this for now.
# https://github.com/explosion/spaCy/issues/7664
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'
###########################################


class DataSet(Dataset):

    def __init__(self,data_folder,image_size, transforms, classes_path=None):

        self.data_folder=data_folder
        self.image_size=image_size
        self.dataset=dset.ImageFolder(root=data_folder,  transform=transforms)

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
        user_edit_arr, _ = self.paired_dataset[idx] # p: (data, label).
        if user_edit_arr is None: # this image has no paired data, just return the original image
            return self.dataset[idx]

        return self.get_aug_image(self.dataset[idx][0], user_edit_arr), self.dataset[idx][1]


    def get_aug_image(self, image, user_edit):
        """
        Args:
            image: the original image tensor of shape (3, size, size)
            user_edit: numpy array or pytorch tensor of shape (size, size)
            mode: how to augment the data
        Returns:
            a new image of shape (3, 28, 28), with background filled according to `mode`
        """
        if type(user_edit) != torch.tensor:
            user_edit = torch.tensor(user_edit)

        user_edit = torch.stack([user_edit, user_edit, user_edit]) # Expand to RGB repr of shape (3, size, size)

        new_image = image.clone() # clone the image to avoid pollution
        new_image[user_edit == 1] = 0 # the area marked by the user is the background and should be cleared

        if self.mode == 'mixture':
            mode_idx = np.random.randint(len(self.MIXTURE_METHODS))
            mode = self.mixture_methods[mode_idx]
        else:
            mode = self.mode

        bg_data = get_aug_background(user_edit, mode)  # (N, 1, 28, 28, 3)
        new_image = new_image + bg_data

        return new_image


def paired_loader(path):
    if os.path.getsize(path):
        arr = np.load(path, allow_pickle=True)
        return arr
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

# Test
if __name__ == '__main__':

    dsroot = "./dataset/ten"
    LOAD_PAIRED = True

    if LOAD_PAIRED:
        x = PairedDataset("{}/train".format(dsroot), "{}/paired".format(dsroot), 224, None, 'random_pure')
        print("First image info: {}".format(x.paired_dataset.imgs[0]))
    else:
        x = DataSet("{}/train".format(dsroot), 224)
        print("First image info: {}".format(x.dataset.imgs[0]))


    # print(x.paired_dataset)
    # print(x.paired_dataset[0])
    """
    for i in range(50000):
        if x.paired_dataset[i][0] is not None:
            print('hey')
    """
    import matplotlib.pyplot as plt

    transform = transforms.Compose([
    transforms.ToTensor(),
    # transforms.Normalize(mean=(0.5, 0.5, 0.5),
    #                      std=(0.5, 0.5, 0.5))
    ])

    data_loader = torch.utils.data.DataLoader(x, batch_size=1, shuffle=False, num_workers=1)

    count = 2
    for idx, data in enumerate(data_loader):
        if idx == count:
            if LOAD_PAIRED:
                img = data[0][0].squeeze(0).permute(1,2,0).numpy()
                paired = data[1][0].squeeze(0).permute(1,2,0).numpy()
                label = data[0][1].squeeze(0)
                img = paired
            else:
                img = data[0].squeeze(0).permute(1,2,0).numpy()
                label = data[1].squeeze(0)


            img = transform(img)
            img = np.swapaxes(img, 0, 1)
            img = np.swapaxes(img, 1, 2)
            # print(img)
            plt.imshow(img.numpy())
            plt.show()
            break

