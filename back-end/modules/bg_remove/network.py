# Code adopted from https://github.com/OPHoperHPO/image-background-remove-tool
import os
import time
import os.path as osp
import numpy as np
from PIL import Image, ImageOps
import torch
from torch.autograd import Variable
from .u2net import U2NET as U2NET_DEEP
from .u2net import U2NETP as U2NETP_DEEP
from objects.RDataManager import SquarePad
from torchvision import transforms

def download(url, saveTo, msg=None):
    from urllib import request
    if msg:
        print(msg)
    request.urlretrieve(url, saveTo)

class U2NET:
    """U^2-Net model interface"""

    def __init__(self, device, checkpoint, name="u2net"):
        self.Variable = Variable
        self.torch = torch
        self.device = device
        self.U2NET_DEEP = U2NET_DEEP
        self.U2NETP_DEEP = U2NETP_DEEP
        self.image_size = 320  # required by U2Net
        self.resize_transform = transforms.Compose([
            SquarePad('short_side'), # TODO: Hard-coded for now
            transforms.Resize((self.image_size, self.image_size)),
        ])
        
        if name == 'u2net':  # Load model
            if not osp.exists(checkpoint):
                download(
                    "https://github.com/OPHoperHPO/image-background-remove-tool/releases/download/3.2/u2net.pth",
                    checkpoint,
                    "Downloading U2NET model (176.6mb)..."
                )
            print("Loading a U2NET model (176.6 mb) with better quality but slower processing.")
            net = self.U2NET_DEEP()
        elif name == 'u2netp':
            if not osp.exists(checkpoint):
                download(
                    "https://github.com/OPHoperHPO/image-background-remove-tool/releases/download/3.2/u2netp.pth",
                    checkpoint,
                    "Downloading U2NETp model (4 mb)..."
                )
            print("Loading a U2NETp model (4 mb) with lower quality but fast processing.")
            net = self.U2NETP_DEEP()
        else:
            raise NotImplementedError("Unknown u2net model!")

        try:
            if device == 'cpu':
                net.load_state_dict(self.torch.load(os.path.join(checkpoint), map_location='cpu'))
            else:
                net.load_state_dict(self.torch.load(os.path.join(checkpoint)))
                net = net.to(device)
        except FileNotFoundError:
            raise FileNotFoundError("No pre-trained model found!")
        net.eval()
        self.__net__ = net  # Define model

    def process_image(self, data, preprocessing=None, postprocessing=None):
        """
        Removes background from image and returns PIL RGBA Image.
        :param data: Path to image or PIL image
        :param preprocessing: Image Pre-Processing Algorithm Class (optional)
        :param postprocessing: Image Post-Processing Algorithm Class (optional)
        :return: PIL RGB Image. If an error reading the image is detected, returns False.
        """
        if isinstance(data, str):
            print("Load image: {}".format(data))
        image, org_image = self.__load_image__(data)  # Load image
        if image is False or org_image is False:
            return False
        if preprocessing:  # If an algorithm that preprocesses is specified,
            # then this algorithm should immediately remove the background
            image = preprocessing.run(self, image, org_image)
        else:
            image = self.__get_output__(image, org_image)  # If this is not, then just remove the background
        if postprocessing:  # If a postprocessing algorithm is specified, we send it an image without a background
            image = postprocessing.run(self, image, org_image)
        return image

    def __get_output__(self, image, org_image):
        """
        Returns output from a neural network
        :param image: Prepared Image
        :param org_image: Original pil image
        :return: Image without background
        """
        start_time = time.time()  # Time counter
        image = image.type(self.torch.FloatTensor)
        image = self.Variable(image.to(self.device))

        mask, d2, d3, d4, d5, d6, d7 = self.__net__(image)  # Predict mask
        print("Mask prediction completed")
        # Normalization
        print("Mask normalization")
        mask = mask[:, 0, :, :]
        mask = self.__normalize__(mask)
        # Prepare mask
        print("Prepare mask")
        mask = self.__prepare_mask__(mask, org_image.size)
        # Apply mask to image
        print("Apply mask to image")
        empty = Image.new("RGBA", org_image.size)
        empty.paste((255, 255, 255, 255), [0, 0, empty.size[0], empty.size[1]])
        image = Image.composite(org_image, empty, mask)
        print("Finished! Time spent: {}".format(time.time() - start_time))

        # np.set_printoptions(threshold=np.inf)
        # print(np.array(image))

        return image.convert("RGB")

    def __load_image__(self, data):
        """
        Loads an image file for other processing
        :param data: Path to image file or PIL image
        :return: image tensor, original pil image
        """
        if isinstance(data, str):
            try:
                # TODO: use existing library instead!
                pil_image = Image.open(data)  # Load image if there is a path 
                if pil_image.mode != 'RGB':
                    pil_image = pil_image.convert('RGB')
            except IOError:
                print('Cannot retrieve image. Please check file: ' + data)
                return False, False
            image = np.asarray(self.resize_transform(pil_image), dtype=np.float64)
        else:
            image = np.array(self.resize_transform(data), dtype=np.float64)  # Convert PIL image to numpy arr
            pil_image = data
        
        image = self.__ndrarray2tensor__(image)  # Convert image from numpy arr to tensor
        
        return image, pil_image

    def __ndrarray2tensor__(self, image: np.ndarray):
        """
        Converts a NumPy array to a tensor
        :param image: Image numpy array
        :return: Image tensor
        """
        tmp_img = np.zeros((image.shape[0], image.shape[1], 3))
        image /= np.max(image)
        if image.shape[2] == 1:
            tmp_img[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
            tmp_img[:, :, 1] = (image[:, :, 0] - 0.485) / 0.229
            tmp_img[:, :, 2] = (image[:, :, 0] - 0.485) / 0.229
        else:
            tmp_img[:, :, 0] = (image[:, :, 0] - 0.485) / 0.229
            tmp_img[:, :, 1] = (image[:, :, 1] - 0.456) / 0.224
            tmp_img[:, :, 2] = (image[:, :, 2] - 0.406) / 0.225
        tmp_img = tmp_img.transpose((2, 0, 1))
        tmp_img = np.expand_dims(tmp_img, 0)
        return self.torch.from_numpy(tmp_img)

    def __normalize__(self, predicted):
        """Normalize the predicted map"""
        ma = self.torch.max(predicted)
        mi = self.torch.min(predicted)
        out = (predicted - mi) / (ma - mi)
        return out

    @staticmethod
    def __prepare_mask__(predict, image_size):
        """Prepares mask
        Returns a mask as an PIL image 
        """
        predict = predict.squeeze()
        predict_np = predict.cpu().data.numpy()
        mask = Image.fromarray(predict_np * 255).convert("1")
        mask = mask.resize(image_size, resample=Image.BILINEAR)
        return mask