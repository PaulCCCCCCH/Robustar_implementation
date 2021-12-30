import torch
import time
from torchattacks import PGD
import os


class Trainer():
    storeArr = None
    device = "cpu"
    updateInfo = None
    PATH = "temp_path"
    statusInfo = {}

    def __init__(self, net, trainset, testset, batch_size, shuffle, num_workers, device, learn_rate, auto_save, save_dir, name, use_paired_train=False, paired_reg=1e-4):
        self.initialize_loader(
            trainset, testset, batch_size, shuffle, num_workers)
        self.net = net
        self.device = device
        self.learn_rate = learn_rate
        self.auto_save = auto_save
        self.save_dir = save_dir
        self.name = name
        self.use_paired_train = use_paired_train
        self.paired_reg = paired_reg
        self.stop = False

        # Start the tensorboard

    def initialize_loader(self, trainset, testset, batch_size, shuffle, num_workers):
        self.testloader = torch.utils.data.DataLoader(
            testset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
        self.trainloader = torch.utils.data.DataLoader(
            trainset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)

    def start_train(self, call_back, epochs, auto_save):
        self.updateInfo = call_back
        self.train(epochs, True, auto_save, False, 1)

    def update_gui(self):
        self.updateInfo(self.statusInfo)

    def save_net_acc(self, acc):
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)
        torch.save(self.net.state_dict(), os.path.join(
            self.save_dir, self.name + "_" + str(float(acc))[:4]))

    def get_correct(self):
        correct_result = []
        incorrect_result = []

        loader = self.testloader
        torch.no_grad()
        total = 0
        self.net.eval()

        # trainer.testloader.dataset.dataset.samples[0]

        # for data in loader:
        for data in self.storeLoader(loader):
            images, labels = data
            images, labels = images.to(self.device), labels.to(self.device)
            outputs = self.net(images)

            _, predicted = torch.max(outputs.data, 1)

            # 将正确和错误的文件名存起来
            for i in range(len(labels)):
                fileName = loader.dataset.dataset.samples[total+i]
                if labels[i] == predicted[i]:
                    correct_result.append(fileName)
                else:
                    incorrect_result.append(fileName)

            total += labels.size(0)
        torch.cuda.empty_cache()
        return correct_result, incorrect_result

    def get_test_result(self):
        result = []

        loader = self.testloader
        torch.no_grad()
        self.net.eval()

        # trainer.testloader.dataset.dataset.samples[0]

        # for data in loader:
        for data in self.storeLoader(loader):
            images, labels = data
            images, labels = images.to(self.device), labels.to(self.device)
            outputs = self.net(images)

            _, predicted = torch.max(outputs.data, 1)

            for i in range(len(labels)):
                result.append([labels[i].cpu().numpy().tolist(), predicted[i].cpu(
                ).numpy().tolist(), outputs.data[i].cpu().numpy().tolist()])
        torch.cuda.empty_cache()
        return result

    def print_accuracy(self):
        loader = self.testloader
        torch.no_grad()
        correct = 0
        total = 0
        self.net.eval()

        # for data in loader:
        for data in self.storeLoader(loader):
            images, labels = data
            images, labels = images.to(self.device), labels.to(self.device)
            outputs = self.net(images)

            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum()

        result = 1.0 * 100 * correct / total
        self.statusInfo['test_acc'] = float(result)
        self.update_gui()
        print('The accuracy is: %.3f%%' % result)
        torch.cuda.empty_cache()
        return result

    def storeLoader(self, loader):
        if self.storeArr:
            return self.storeArr
        self.storeArr = []
        for _, data in enumerate(loader, 0):
            self.storeArr.append(data)
        return self.storeArr

    def returna(self, a, b):
        return a

    def train(self, epoch, debug_info=True, save_best=True, pgd=False, merge=1):
        starttime = time.time()
        loader = self.trainloader
        criterion = torch.nn.CrossEntropyLoss()
        pgd_attack = PGD(self.net, eps=0.2, alpha=2/255,
                         iters=2) if pgd else self.returna
        optimizer = torch.optim.SGD(self.net.parameters(
        ), lr=self.learn_rate, momentum=0.9, weight_decay=5e-4)
        best = 0
        for epoch in range(epoch):
            print('\nEpoch: %d' % (epoch + 1))
            self.net.train()
            sum_loss = 0.0
            correct = 0.0
            total = 0.0
            length = len(loader)
            # storeLoader(loader)
            optimizer.zero_grad()
            for i, data in enumerate(loader, 0):

                if self.stop:
                    endtime = time.time()
                    print("Time consumption:", endtime-starttime)
                    print("Trainning stopped!")
                    return 
                    

                if self.use_paired_train:
                    inputs, labels = data[0]
                    paired_inputs, _ = data[1]
                    paired_inputs = paired_inputs.to(self.device)
                else:
                    inputs, labels = data

                inputs = pgd_attack(inputs, labels)
                inputs, labels = inputs.to(self.device), labels.to(self.device)

                # forward + backward
                outputs = self.net(inputs)
                loss = criterion(outputs, labels)

                if self.use_paired_train:
                    paired_outputs = self.net(paired_inputs)
                    paired_loss = criterion(paired_outputs, labels)
                    loss += paired_loss + self.paired_reg * \
                        torch.mean(torch.square(
                            torch.norm(outputs - paired_outputs)))

                loss.backward()

                if i % merge == 0 and i != 0:
                    optimizer.step()
                    optimizer.zero_grad()

                # print the accuracy
                sum_loss += loss.item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += predicted.eq(labels.data).cpu().sum()

                info_iteration = i + 1 + epoch * length
                info_loss = sum_loss / (i + 1)
                info_train_acc = 100. * correct / total

                self.statusInfo['epoch'] = epoch + 1
                self.statusInfo['iter'] = info_iteration
                self.statusInfo['loss'] = info_loss
                self.statusInfo['train_acc'] = info_train_acc

                output_text = ('[epoch:%d, iter:%d] Loss: %.03f | Acc: %.3f%% '
                               % (epoch + 1, info_iteration, info_loss, info_train_acc))
                self.writer.add_scalar(
                    'train accuracy', info_train_acc, info_iteration)
                self.writer.add_scalar('loss', info_loss, info_iteration)

                self.update_gui()

                print('\r'+output_text, flush=True, end='')
            # save_net(net)
            print("Epoch Finish!")
            torch.cuda.empty_cache()
            if(debug_info):
                current_acc = self.print_accuracy()
                torch.cuda.empty_cache()
                if current_acc > best:
                    if save_best:
                        self.save_net_acc(current_acc)
                    best = current_acc

        endtime = time.time()
        print("Time consumption:", endtime-starttime)
