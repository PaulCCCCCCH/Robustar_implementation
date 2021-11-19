from flashtorch_.utils import apply_transforms,load_image
from flashtorch_.saliency import Backprop
import torch,matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# https://github.com/MisaOgura/flashtorch#saliency-maps-flashtorchsaliency
def visualize(mymodel,imgpath,imgsize):

        backprop=Backprop(mymodel)
        image=load_image(imgpath)
        image=apply_transforms(image,imgsize)

        modeloutput=backprop.model(image)
        modeloutput=torch.nn.functional.softmax(modeloutput,1)
        
        _,predict=torch.max(modeloutput,1)
        images=backprop.visualize(image,predict,guided=True,return_image=True)

        plt.savefig('img-v.png')
        plt.close('all')

        return modeloutput

if __name__ == '__main__':

        import torchvision,torch
        # from modules.visualize_module.visualize.visual import visualize
        model = torchvision.models.resnet34() 
        output = visualize(model,'/Robustar2/dataset/train/0/0_10008.jpg',32)
        print(output.shape)