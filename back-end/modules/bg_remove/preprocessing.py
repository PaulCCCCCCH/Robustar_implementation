# Code adopted from https://github.com/OPHoperHPO/image-background-remove-tool
# TODO: code not used in current version.
import logging
import time

import numpy as np
from PIL import Image

from strings import PREPROCESS_METHODS

logger = logging.getLogger(__name__)


def method_detect(method: str):
    """Detects which method to use and returns its object"""
    if method == "bbd-fastrcnn":
        return BoundingBoxDetectionFastRcnn()
    else:
        raise NotImplementedError('Unsupported pre processing method')


class BoundingBoxDetectionFastRcnn:
    """
    Class for the image preprocessing method.
    This image pre-processing technique uses two neural networks ($used_model and Fast RCNN)
    to first detect the boundaries of objects in a photograph,
    cut them out, sequentially remove the background from each object in turn
    and subsequently collect the entire image from separate parts
    """

    def __init__(self):
        self.__fast_rcnn__ = FastRcnn()
        self.model = None
        self.prep_image = None
        self.orig_image = None

    @staticmethod
    def trans_paste(bg_img, fg_img, box=(0, 0)):
        """
        Inserts an image into another image while maintaining transparency.
        :param bg_img: Background pil image
        :param fg_img: Foreground pil image
        :param box: Bounding box
        :return: Pil Image
        """
        fg_img_trans = Image.new("RGBA", bg_img.size)
        fg_img_trans.paste(fg_img, box, mask=fg_img)
        new_img = Image.alpha_composite(bg_img, fg_img_trans)
        return new_img

    @staticmethod
    def __orig_object_border__(border, orig_image, resized_image, indent=16):
        """
        Rescales the bounding box of an object
        :param indent: The boundary of the object will expand by this value.
        :param border: array consisting of the coordinates of the boundaries of the object
        :param orig_image: original pil image
        :param resized_image: resized image ndarray
        :return: tuple consisting of the coordinates of the boundaries of the object
        """
        x_factor = resized_image.shape[1] / orig_image.size[0]
        y_factor = resized_image.shape[0] / orig_image.size[1]
        xmin, ymin, xmax, ymax = [int(x) for x in border]
        if ymin < 0:
            ymin = 0
        if ymax > resized_image.shape[0]:
            ymax = resized_image.shape[0]
        if xmax > resized_image.shape[1]:
            xmax = resized_image.shape[1]
        if xmin < 0:
            xmin = 0
        if x_factor == 0:
            x_factor = 1
        if y_factor == 0:
            y_factor = 1
        border = (int(xmin / x_factor) - indent,
                  int(ymin / y_factor) - indent, int(xmax / x_factor) + indent, int(ymax / y_factor) + indent)
        return border

    def run(self, model, prep_image, orig_image):
        """
        Runs an image preprocessing algorithm to improve background removal quality.
        :param model: The class of the neural network used to remove the background.
        :param prep_image: Prepared for the neural network image
        :param orig_image: Source image
        :returns: Image without background
        """
        _, resized_image, results = self.__fast_rcnn__.process_image(orig_image)

        classes = self.__fast_rcnn__.class_names
        bboxes = results['bboxes']
        ids = results['ids']
        scores = results['scores']

        object_num = len(bboxes)  # We get the number of all objects in the photo

        if object_num < 1:  # If there are no objects, or they are not found,
            # we try to remove the background using standard tools
            return model.__get_output__(prep_image, orig_image)
        else:
            # Check that all arrays match each other in size
            if ids is not None and not len(bboxes) == len(ids):
                return model.__get_output__(prep_image,
                                            orig_image)  # we try to remove the background using standard tools
            if scores is not None and not len(bboxes) == len(scores):
                return model.__get_output__(prep_image, orig_image)
                # we try to remove the background using standard tools
        objects = []
        for i, bbox in enumerate(bboxes):
            if scores is not None and scores.flat[i] < 0.5:
                continue
            if ids is not None and ids.flat[i] < 0:
                continue
            object_cls_id = int(ids.flat[i]) if ids is not None else -1
            if classes is not None and object_cls_id < len(classes):
                object_label = classes[object_cls_id]
            else:
                object_label = str(object_cls_id) if object_cls_id >= 0 else ''
            object_border = self.__orig_object_border__(bbox, orig_image, resized_image)
            objects.append([object_label, object_border])
        if objects:
            if len(objects) == 1:
                return model.__get_output__(prep_image, orig_image)
                # we try to remove the background using standard tools
            else:
                obj_images = []
                for obj in objects:
                    border = obj[1]
                    obj_crop = orig_image.crop(border)
                    # TODO: make a special algorithm to improve the removal of background from images with people.
                    if obj[0] == "person":
                        obj_img = model.process_image(obj_crop)
                    else:
                        obj_img = model.process_image(obj_crop)
                    obj_images.append([obj_img, obj])
                image = Image.new("RGBA", orig_image.size)
                for obj in obj_images:
                    image = self.trans_paste(image, obj[0], obj[1][1])
                return image
        else:
            return model.__get_output__(prep_image, orig_image)