from ..flashtorch_.utils import apply_transforms, load_image
from ..flashtorch_.saliency import Backprop
import torch, matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt


# https://github.com/MisaOgura/flashtorch#saliency-maps-flashtorchsaliency
def visualize(mymodel, imgpath, imgsize, device):
    backprop = Backprop(mymodel)
    image = load_image(imgpath)
    image = apply_transforms(image, imgsize)

    modeloutput = backprop.model(image.to(device))
    modeloutput = torch.nn.functional.softmax(modeloutput, 1)

    _, predict = torch.max(modeloutput, 1)
    use_gpu = device != 'cpu'
    images = backprop.visualize(image, predict, guided=True, return_image=True, use_gpu=use_gpu)

    return images


if __name__ == '__main__':
    # test
    import torchvision, torch

    # from modules.visualize_module.visualize.visual import visualize
    model = torchvision.models.resnet34()
    output = visualize(model, '/Robustar2/dataset/train/n01440764/ILSVRC2012_val_00000293.JPEG', 32)
    print(len(output))
    for i in range(len(output)):
        print(output[i])
        plt.figure(output[i])
        plt.savefig('/Robustar2/influence_images/train/n01440764/ILSVRC2012_val_00000293_' + str(i) + '.png')
        plt.close()
