import torch
import torchvision
import os
from modules.bg_remove.network import U2NET


class RAutoAnnotator:

    def __init__(self, device, checkpoint=None, model_name="u2net"):
        """
        name can either be "u2net" (176 mb) or "u2netp" (4 mb).
        """
        if "u2net" in model_name:
            self.model = U2NET(device, checkpoint, model_name)
        else:
            raise NotImplementedError("Only support u2net model for background removal")

        # We ignore pre and post processing for now

    def annotate_single(self, imagePath: str, imageSize: int):
        """
        returns a PIL image in RGB
        """
        return self.model.process_image(imagePath)

    def annotate_batch(self, images: list, savedir: str):
        # TODO
        pass

