from objects.RModelWrapper import RModelWrapper
from objects.RServer import RServer
from ..flashtorch_.utils import apply_transforms, load_image
from ..flashtorch_.saliency import Backprop
import torch


# https://github.com/MisaOgura/flashtorch#saliency-maps-flashtorchsaliency
def visualize(model_wrapper: RModelWrapper, imgpath, imgsize, device):
    mymodel = model_wrapper.model
    images = []
    try:
        backprop = Backprop(mymodel)
        image = load_image(imgpath)

        dataManager = RServer.get_data_manager()
        transform = dataManager.transforms

        image = apply_transforms(image, transform, imgsize)

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
