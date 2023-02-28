from utils import get_default_config,init_logging
from calc_influence_function import calc_influence_single
import torch,torchvision
import torchvision.transforms as transforms

if __name__ == "__main__":
    config = get_default_config()
    model=torchvision.models.resnet18()
    model.cuda()

    transform_set = transforms.Compose([
            transforms.Resize([32, 32]),
            transforms.ToTensor(),
            transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
        ])

    trainset=torchvision.datasets.ImageFolder(root='C:/Users/donlin/Documents/GitHub/Robustar2/dataset/cifar/train', transform=transform_set)
    testset=torchvision.datasets.ImageFolder(root='C:/Users/donlin/Documents/GitHub/Robustar2/dataset/cifar/test', transform=transform_set)

    trainloader = torch.utils.data.DataLoader(trainset, batch_size=6, shuffle=False, num_workers=1)
    testloader = torch.utils.data.DataLoader(testset, batch_size=6, shuffle=False, num_workers=1)

    influence, harmful, helpful, _ = calc_influence_single(
            model, trainloader, testloader, test_id_num=0, gpu=config['gpu'],
            recursion_depth=config['recursion_depth'], r=config['r_averaging'])
