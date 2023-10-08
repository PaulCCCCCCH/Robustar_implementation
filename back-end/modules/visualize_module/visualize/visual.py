from objects.RModelManager import RModelManager
from ..flashtorch_.utils import apply_transforms, load_image
from ..flashtorch_.saliency import Backprop
import torch


# https://github.com/MisaOgura/flashtorch#saliency-maps-flashtorchsaliency
def visualize(model_manager: RModelManager, imgpath, imgsize, device):
    mymodel = model_manager.model
    images = []
    try:
        backprop = Backprop(mymodel)
        image = load_image(imgpath)
        image = apply_transforms(image, imgsize)

        modeloutput = backprop.model(image.to(device))
        modeloutput = torch.nn.functional.softmax(modeloutput, 1)

        _, predict = torch.max(modeloutput, 1)
        use_gpu = device != "cpu"
        images = backprop.visualize(
            image, predict, guided=True, return_image=True, use_gpu=use_gpu
        )
        backprop.unregister_hooks()
    except Exception as e:
        print(str(e))

    return images
