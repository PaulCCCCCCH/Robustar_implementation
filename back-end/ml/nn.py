import torch,torchvision,torch.nn,time
import torchvision.transforms as transforms
import torchvision.datasets as dset
from torchattacks import PGD, FGSM

class CifarSet:

    BATCH_SIZE=128
    MERGE_BATCH=1
    #>50 <100
    LEARN_RATE=0.01
    THREAD_NUM=6
    test_folder='./dataset/cifar_test'
    train_folder='./dataset/cifar_train'
    classes = ['plane', 'car', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck']

    transform_set = transforms.Compose([
        transforms.Resize([32, 32]),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    testset=dset.ImageFolder(root=test_folder,  transform=transform_set)

    trainset=dset.ImageFolder(root=train_folder,  transform=transform_set)


    def initialize_loader(self):
        self.testloader = torch.utils.data.DataLoader(self.testset, batch_size=self.BATCH_SIZE, shuffle=True, num_workers=self.THREAD_NUM)
        self.trainloader = torch.utils.data.DataLoader(self.trainset, batch_size=self.BATCH_SIZE, shuffle=True, num_workers=self.THREAD_NUM)
    #need implement

    def __init__(self):
        print('cifar-10 dataset load success')


class ImageNetSet:

    BATCH_SIZE=10
    MERGE_BATCH=10
    #>50 <100
    LEARN_RATE=0.01
    THREAD_NUM=6
    test_folder='./dataset/imagenet_test'
    train_folder='./dataset/imagenet_train'
    classes = ['tench', 'english springer', 'cassette_player', 'chain saw','church', 'french horn', 'garbage truck', 'gas pump', 'golf ball', 'parachute']

    transform_set = transforms.Compose([
        transforms.Resize([224, 224]),
        transforms.ToTensor(),
        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))
    ])

    testset=dset.ImageFolder(root=test_folder,  transform=transform_set)
    trainset=dset.ImageFolder(root=train_folder,  transform=transform_set)

    def initialize_loader(self):
        self.testloader = torch.utils.data.DataLoader(self.testset, batch_size=self.BATCH_SIZE//3, shuffle=True, num_workers=self.THREAD_NUM)
        self.trainloader = torch.utils.data.DataLoader(self.trainset, batch_size=self.BATCH_SIZE, shuffle=True, num_workers=self.THREAD_NUM)

    def __init__(self):
        print('ImageNet subset load success')

class Resnet18:
    device = torch.device("cpu" )#'cpu' 'cuda'
    
    def init_net(self,network_type=-1):
        if network_type==0:
            self.net=torchvision.models.resnet18(pretrained=False).to(self.device)
            self.net.PATH='./model/resnet18_imagenet_model.pth'
        if network_type==1:
            self.net=torchvision.models.resnet18(pretrained=False).to(self.device)
            self.net.PATH='./model/resnet18pgd_imagenet_model.pth'
        if network_type==2:
            self.net=torchvision.models.ResNet(torchvision.models.resnet.BasicBlock, [2, 2, 2, 2],num_classes=10)
            self.net.conv1 = torch.nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1,bias=False)
            self.net.maxpool=torch.nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
            self.net.PATH='./model/resnet18_cifar_model.pth'
        if network_type==3:
            self.net=torchvision.models.ResNet(torchvision.models.resnet.BasicBlock, [2, 2, 2, 2],num_classes=10)
            self.net.conv1 = torch.nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1,bias=False)
            self.net.maxpool=torch.nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
            self.net.PATH='./model/resnet18pgd_cifar_model.pth'
        if network_type==4:
            self.net=torchvision.models.ResNet(torchvision.models.resnet.BasicBlock, [2, 2, 2, 2],num_classes=10)
            self.net.conv1 = torch.nn.Conv2d(3, 64, kernel_size=3, stride=1, padding=1,bias=False)
            self.net.PATH='./model/resnet18_cifar_model.pth'
            #self.net.maxpool=torch.nn.MaxPool2d(kernel_size=3, stride=1, padding=1)
        return self

    def load_net(self):
        path=self.net.PATH
        print('load net from: ',path)
        self.net.load_state_dict(torch.load(path,map_location=self.device))
        return self

    def apply_cuda(self):
        self.device = torch.device("cuda")
        if self.net:
            self.net=self.net.to(self.device)
        return self

    def get_net(self):
        return self.net
        
    def save_net(self):
        torch.save(self.net.state_dict(), self.net.PATH)
        return self

class Trainer(Resnet18):
    dataset=None
    storeArr=None
    
    def __init__(self,dataset):
        self.dataset=dataset
        dataset.initialize_loader()

        
    def save_net_acc(self,acc):
        torch.save(self.net.state_dict(), './best/'+self.net.PATH+str(float(acc))[:4])

        
    def print_accuracy(self):
        loader=self.dataset.testloader
        torch.no_grad()
        correct = 0
        total = 0
        self.net.eval()
        
        #for data in loader:
        for data in self.storeLoader(loader):
            images, labels = data
            images, labels = images.to(self.device), labels.to(self.device)
            outputs = self.net(images)
            
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum()
            
        result=1.0 * 100 * correct / total
        print('The accuracy is: %.3f%%' % result)
        torch.cuda.empty_cache()
        return result


    def storeLoader(self,loader):
        if self.storeArr:
            return self.storeArr
        self.storeArr=[]
        for _, data in enumerate(loader, 0):
            self.storeArr.append(data)
        return self.storeArr


    def returna(self,a,b):
        return a
                    
    def train(self,epoch,debug_info=True,save_best=True,pgd=False,merge=1):
        starttime=time.time()
        loader=self.dataset.trainloader
        print("Start Training")
        criterion = torch.nn.CrossEntropyLoss()
        pgd_attack = PGD(self.net, eps=0.2, alpha=2/255, iters=2) if pgd else self.returna
        optimizer = torch.optim.SGD(self.net.parameters(), lr=self.dataset.LEARN_RATE, momentum=0.9, weight_decay=5e-4)
        best=0
        for epoch in range(epoch):
            print('\nEpoch: %d' % (epoch + 1))
            self.net.train()
            sum_loss = 0.0
            correct = 0.0
            total = 0.0
            length = len(loader)
            #storeLoader(loader)
            optimizer.zero_grad()
            for i, data in enumerate(loader, 0):
            
                inputs, labels = data
                inputs = pgd_attack(inputs, labels)
                inputs, labels = inputs.to(self.device), labels.to(self.device)

                # forward + backward
                outputs = self.net(inputs)
                loss = criterion(outputs, labels)
                loss.backward()
                
                if i%merge==0 and i!=0:
                    optimizer.step()
                    optimizer.zero_grad()

                # print the accuracy
                sum_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += predicted.eq(labels.data).cpu().sum()
                output_text=('[epoch:%d, iter:%d] Loss: %.03f | Acc: %.3f%% '
                    % (epoch + 1, (i + 1 + epoch * length), sum_loss / (i + 1), 100. * correct / total))
                print('\r'+output_text,flush=True,end='')
            #save_net(net)
            print("Epoch Finish!")
            torch.cuda.empty_cache()
            if(debug_info):
                current_acc=self.print_accuracy()
                torch.cuda.empty_cache()
                if current_acc>best:
                    if save_best:
                        self.save_net_acc(current_acc)
                    best=current_acc
                    
        endtime=time.time()
        print("Time consumption:",endtime-starttime)


class DataModel:
    cifar10_dataset  = None
    imagenet_dataset = None
    
    imagenet_resnet18_net     = None
    imagenet_resnet18_pgd_net = None
    cifar10_resnet18_net      = None
    cifar10_resnet18_cuda_net = None
    cifar10_resnet18_pgd_net  =None
    
    def __init__(self):
        self.cifar10_dataset  = CifarSet()
        self.imagenet_dataset = ImageNetSet()
        
        self.imagenet_resnet18_net     = Resnet18().init_net(0).load_net().get_net()
        self.imagenet_resnet18_pgd_net = Resnet18().init_net(1).load_net().get_net()
        self.cifar10_resnet18_net      = Resnet18().init_net(2).load_net().get_net()
        self.cifar10_resnet18_pgd_net  = Resnet18().init_net(3).load_net().get_net()
        

    def get_model(self,modelid,datasetid):
        if datasetid==0:
            if modelid==0:
                return self.imagenet_resnet18_net
            if modelid==1:
                return self.imagenet_resnet18_pgd_net
        if datasetid==1:
            if modelid==0:
                return self.cifar10_resnet18_net
            if modelid==1:
                return self.cifar10_resnet18_pgd_net
        raise Exception("Invalid datasetid or Invalid modelid!",datasetid,modelid)

    def get_dataset(self,datasetid,isTestset):
        if datasetid==0:
            if isTestset:
                return self.imagenet_dataset.testset,224,self.imagenet_dataset.classes
            else:
                return self.imagenet_dataset.trainset,224,self.imagenet_dataset.classes
        if datasetid==1:
            if isTestset:
                return self.cifar10_dataset.testset,32,self.cifar10_dataset.classes
            else:
                return self.cifar10_dataset.trainset,32,self.cifar10_dataset.classes
        raise Exception("Invalid datasetid!",datasetid)


if __name__=="__main__":

    d=CifarSet()
    t=Trainer(d)
    
    #t.init_net(3)
    #t.apply_cuda()
    #t.train(100,debug_info=True,save_best=True,pgd=True,merge=d.MERGE_BATCH)

    for lr in [0.1]:
        t.init_net(3)
        t.apply_cuda()
        d.LEARN_RATE=lr
        print('learn rate',d.LEARN_RATE)
        t.train(15,debug_info=True,save_best=False,merge=d.MERGE_BATCH)
        d.LEARN_RATE=lr/10
        print('learn rate',d.LEARN_RATE)
        t.train(15,debug_info=True,save_best=False,merge=d.MERGE_BATCH)
        d.LEARN_RATE=lr/100
        print('learn rate',d.LEARN_RATE)
        t.train(15,debug_info=True,save_best=False,merge=d.MERGE_BATCH)
    exit()

    for i in [0,1]:
        #net.PATH+='PGD'
        
        init_net(i)
        apply_cuda()
        train(2,debug_info=True,save_best=False,merge=MERGE_BATCH)
        #train(100,debug_info=True,save_best=True,merge=MERGE_BATCH)
        