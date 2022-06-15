import torch
import torchvision
import os

IMAGENET_OUTPUT_SIZE = 1000


class RModelWrapper:
    # model=Model("resnet-18-32x32",'./model/weight/resnet18_cifar_model.pth','cpu')
    def __init__(self, network_type, net_path, device, pretrained, num_classes):
        # self.device = torch.device(device)
        if pretrained:
            assert num_classes == IMAGENET_OUTPUT_SIZE, f"Pretrained model is supposed to have {IMAGENET_OUTPUT_SIZE} classes as output. "
        self.device = device  # We keep device as string to allow for easy comparison
        self.init_model(network_type, pretrained, num_classes)
        self.modelwork_type = network_type
        if os.path.exists(net_path):
            print('Loading previous checkpoint at {}'.format(net_path))
            self.load_net(net_path)
        else:
            print('Checkpoint file not found: {}'.format(net_path))

        # Duplicated code
        # if 'cuda' in device:
        #     self.apply_cuda()

    def init_model(self, network_type, pretrained, num_classes):
        if network_type == 'resnet-18':
            self.model = torchvision.models.resnet18(
                pretrained=pretrained, num_classes=num_classes).to(self.device)
        elif network_type == 'resnet-34':
            self.model = torchvision.models.resnet34(pretrained=pretrained, num_classes=num_classes).to(self.device)
        elif network_type == 'resnet-50':
            self.model = torchvision.models.resnet50(pretrained=pretrained, num_classes=num_classes).to(self.device)
        elif network_type == 'resnet-101':
            self.model = torchvision.models.resnet101(pretrained=pretrained, num_classes=num_classes).to(self.device)
        elif network_type == 'resnet-152':
            self.model = torchvision.models.resnet152(pretrained=pretrained, num_classes=num_classes).to(self.device)
        elif network_type == 'mobilenet-v2':
            self.model = torchvision.models.mobilenet_v2(pretrained=pretrained, num_classes=num_classes).to(self.device)
        elif network_type == 'resnet-18-32x32':
            self.model = torchvision.models.ResNet(torchvision.models.resnet.BasicBlock, [2, 2, 2, 2],
                                                   num_classes=num_classes)
            self.model.conv1 = torch.nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1, bias=False)
            self.model.maxpool = torch.nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
            self.model = self.model.to(self.device)
        elif network_type == 'alexnet':
            self.model = torchvision.models.alexnet(pretrained=pretrained, num_classes=num_classes).to(self.device)
        else:
            raise NotImplementedError("Requested model type not supported. Please check.")

    def load_net(self, path):
        if os.path.exists(path):
            print('load net from: ', path)
            self.model.load_state_dict(torch.load(
                path, map_location=self.device))
        else:
            print('weight file not found')

    # Duplicated code
    # def apply_cuda(self):
    #     self.device = torch.device(self.device)
    #     if self.model:
    #         self.model = self.model.to(self.device)
    #     return self
