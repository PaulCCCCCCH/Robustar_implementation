from modules.visualize_module.flashtorch_.utils import apply_transforms, load_image
from modules.visualize_module.flashtorch_.saliency import Backprop

import torch,matplotlib
import torchvision.transforms as transforms
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def visualize(mymodel,imgpath,imgsize):

        backprop=Backprop(mymodel)
        image=load_image(imgpath)

        # image = do_transform(image,transform)
        image=apply_transforms(image,imgsize)

        modeloutput=backprop.model(image)
        modeloutput=torch.nn.functional.softmax(modeloutput,1)

        _,predict=torch.max(modeloutput,1)

        # TODO: Save images to visualization folder, or save them in the server buffer and return
        images=backprop.visualize_with_four_output(image,predict,guided=True,return_image=True)

        return modeloutput[0]


