import torch
import time
from torchattacks import PGD
import os
from objects.RTask import RTask, TaskType
from objects.RServer import RServer
import copy
import multiprocessing


class Trainer():
    storeArr = None
    device = "cpu"
    updateInfo = None
    PATH = "temp_path"
    statusInfo = {}

    def __init__(self, net, trainset, testset, batch_size, shuffle, num_workers, device, learn_rate, auto_save, save_every, save_dir, name, use_paired_train=False, paired_reg=1e-4):
        self.initialize_loader(
            trainset, testset, batch_size, shuffle, num_workers)
        self.net = net
        self.device = device
        self.learn_rate = learn_rate
        self.auto_save = auto_save
        self.save_every = save_every
        self.save_dir = save_dir
        self.name = name
        self.use_paired_train = use_paired_train
        self.paired_reg = paired_reg


    def initialize_loader(self, trainset, testset, batch_size, shuffle, num_workers):
        self.testloader = torch.utils.data.DataLoader(
            testset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
        self.trainloader = torch.utils.data.DataLoader(
            trainset, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)

    def start_train(self, call_back, epochs, auto_save):
        self.updateInfo = call_back
        self.train(epochs, auto_save=auto_save, pgd=False)

    def update_gui(self):
        self.updateInfo(self.statusInfo)

    def _save_net(self, name):
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)
        torch.save(self.net.state_dict(), os.path.join(self.save_dir, name))

        # Save the model to the Rserver instance
        dict_in_mem = copy.deepcopy(self.net.state_dict())

        RServer.addModelWeight(name, dict_in_mem)

    def save_net_best(self):
        name_str = self.name + "_best"
        self._save_net(name_str)

    def save_net_epoch(self, epoch):
        name_str = self.name + "_" + str(epoch)
        self._save_net(name_str)

    # def get_correct(self):
    #     correct_result = []
    #     incorrect_result = []
    #
    #     loader = self.testloader
    #     torch.no_grad()
    #     total = 0
    #     self.net.eval()
    #
    #     # trainer.testloader.dataset.dataset.samples[0]
    #
    #     # for data in loader:
    #     for data in self.storeLoader(loader):
    #         images, labels = data
    #         images, labels = images.to(self.device), labels.to(self.device)
    #         outputs = self.net(images)
    #
    #         _, predicted = torch.max(outputs.data, 1)
    #
    #         # 将正确和错误的文件名存起来
    #         for i in range(len(labels)):
    #             fileName = loader.dataset.dataset.samples[total+i]
    #             if labels[i] == predicted[i]:
    #                 correct_result.append(fileName)
    #             else:
    #                 incorrect_result.append(fileName)
    #
    #         total += labels.size(0)
    #     torch.cuda.empty_cache()
    #     return correct_result, incorrect_result
    #
    # def get_test_result(self):
    #     result = []
    #
    #     loader = self.testloader
    #     torch.no_grad()
    #     self.net.eval()
    #
    #     # trainer.testloader.dataset.dataset.samples[0]
    #
    #     # for data in loader:
    #     for data in self.storeLoader(loader):
    #         images, labels = data
    #         images, labels = images.to(self.device), labels.to(self.device)
    #         outputs = self.net(images)
    #
    #         _, predicted = torch.max(outputs.data, 1)
    #
    #         for i in range(len(labels)):
    #             result.append([labels[i].cpu().numpy().tolist(), predicted[i].cpu(
    #             ).numpy().tolist(), outputs.data[i].cpu().numpy().tolist()])
    #     torch.cuda.empty_cache()
    #     return result

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

    def train(self, epoch, auto_save=True, pgd=False, merge=1):
        starttime = time.time()
        loader = self.trainloader
        criterion = torch.nn.CrossEntropyLoss()
        pgd_attack = PGD(self.net, eps=0.2, alpha=2/255,
                         iters=2) if pgd else self.returna
        optimizer = torch.optim.SGD(self.net.parameters(
        ), lr=self.learn_rate, momentum=0.9, weight_decay=5e-4)
        best = 0

        # init task
        task = RTask(TaskType.Training, epoch*len(loader))

        for epoch in range(epoch):
            print('\nEpoch: %d' % (epoch + 1))
            sepoch = time.time()
            self.net.train()
            sum_loss = 0.0
            correct = 0.0
            total = 0.0
            length = len(loader)
            # storeLoader(loader)
            optimizer.zero_grad()
            for i, data in enumerate(loader, 0):
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

                # update task
                task_update_res = task.update()
                if not task_update_res:
                    endtime = time.time()
                    print("Time consumption:", endtime-starttime)
                    print("Training stopped!")
                    return 

            # save_net(net)
            print("Epoch Finish!")
            eepoch = time.time()
            print("Time consumption in training epoch:{} {}".format(epoch + 1, eepoch - sepoch))
            torch.cuda.empty_cache()
            sepoch = time.time()
            current_acc = self.print_accuracy()
            eepoch = time.time()
            print("Time consumption in testing epoch:{} {}".format(epoch + 1, eepoch - sepoch))
            torch.cuda.empty_cache()
            if current_acc > best:
                if auto_save:
                    self.save_net_best()
                best = current_acc
            if (epoch + 1) % self.save_every == 0:
                self.save_net_epoch(epoch)

        endtime = time.time()
        print("Time consumption:", endtime-starttime)


        # task exit
        task.exit()

        # Stop updating the tensorboard
        self.stop_tb_process()

    def set_tb_process(self, process):
        self.tb_process = process

    def stop_tb_process(self):
        self.tb_process.terminate()
