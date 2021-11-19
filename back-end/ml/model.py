import torch,torchvision,os
class Model:
    #model=Model("resnet-18-32x32",'./model/weight/resnet18_cifar_model.pth','cpu')
    def __init__(self,network_type,net_path,device,pretrained):
        self.device = torch.device(device)
        self.init_net(network_type,pretrained==pretrained)
        self.network_type = network_type
        if(net_path!=""):
            self.load_net(net_path)
        if('cuda' in device):
            self.apply_cuda()

    def init_net(self,network_type,pretrained):
        if network_type=='resnet-18':
            self.net=torchvision.models.resnet18(pretrained=pretrained).to(self.device)
        elif network_type=='resnet-34':
            self.net=torchvision.models.resnet34(pretrained=pretrained).to(self.device)
        elif network_type=='resnet-50':
            self.net=torchvision.models.resnet50(pretrained=pretrained).to(self.device)
        elif network_type=='resnet-101':
            self.net=torchvision.models.resnet101(pretrained=pretrained).to(self.device)
        elif network_type=='resnet-152':
            self.net=torchvision.models.resnet152(pretrained=pretrained).to(self.device)
        elif network_type=='mobilenet-v2':
            self.net=torchvision.models.mobilenet_v2(pretrained=pretrained).to(self.device)
        elif network_type=='resnet-18-32x32':
            self.net=torchvision.models.ResNet(torchvision.models.resnet.BasicBlock, [2, 2, 2, 2],num_classes=10)
            self.net.conv1 = torch.nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1,bias=False)
            self.net.maxpool=torch.nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
        elif network_type=='alexnet':
            self.net=torchvision.models.alexnet(pretrained=pretrained).to(self.device)
        else:
            raise NotImplementedError("Requested model type not supported. Please check.")

        return self

    def load_net(self,path):
        if os.path.exists(path):
            print('load net from: ', path)
            self.net.load_state_dict(torch.load(path,map_location=self.device))
        else:
            print('weight file not found')

    def apply_cuda(self):
        self.device = torch.device("cuda")
        if self.net:
            self.net=self.net.to(self.device)
        return self
