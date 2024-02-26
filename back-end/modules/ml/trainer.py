import torch
import time
from torchattacks import PGD
import os
import uuid
from objects.RTask import RTask, TaskType
from objects.RServer import RServer
from objects.RModelWrapper import RModelWrapper
from datetime import datetime


class Trainer:
    def __init__(
        self,
        model,
        train_set,
        val_set,
        batch_size,
        shuffle,
        num_workers,
        device,
        learn_rate,
        auto_save,
        save_every,
        save_dir,
        use_paired_train=False,
        use_tensorboard=True,
        paired_reg=1e-4,
    ):
        self.val_sample_buffer = None
        self.update_info = None
        self.status_info = {}

        self.model = model
        self.device = device
        self.learn_rate = learn_rate
        self.auto_save = auto_save
        self.save_every = save_every
        self.save_dir = save_dir
        self.use_paired_train = use_paired_train
        self.use_tensorboard = use_tensorboard
        self.paired_reg = paired_reg
        self.orig_metadata = RModelWrapper.convert_metadata_2_dict(
            RServer.get_model_wrapper().get_current_model_metadata()
        )

        self.best_val_acc = 0
        self.best_train_acc = 0  # The train acc at the best val acc
        self.best_epoch = 0
        self.best_path = None

        # Initialize loaders
        self.train_loader = None
        self.val_loader = None
        self.initialize_loader(train_set, val_set, batch_size, shuffle, num_workers)

    def initialize_loader(self, train_set, test_set, batch_size, shuffle, num_workers):
        self.val_loader = torch.utils.data.DataLoader(
            test_set, batch_size=batch_size, shuffle=False, num_workers=num_workers
        )
        self.train_loader = torch.utils.data.DataLoader(
            train_set, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers
        )

    def start_train(self, call_back, epochs, auto_save):
        self.update_info = call_back
        self.train(epochs, auto_save=auto_save, pgd=False)

    def update_gui(self):
        self.update_info(self.status_info)

    def save_weights(self):
        rand_id = str(uuid.uuid4())
        weight_path = os.path.join(self.save_dir, f"{rand_id}.py")
        torch.save(self.model.state_dict(), weight_path)
        return weight_path

    def save_best_weights(self):
        if self.best_path:
            os.remove(self.best_path)
        self.best_path = self.save_weights()

    def save_best_model(self):
        metadata_4_save = self.create_metadata_4_save(
            self.best_epoch, self.best_path, self.best_train_acc, self.best_val_acc
        )
        RServer.get_model_wrapper().create_model(metadata_4_save)

    def save_epoch_model(self, epoch, train_acc, val_acc):
        weight_path = self.save_weights()
        metadata_4_save = self.create_metadata_4_save(
            epoch, weight_path, train_acc, val_acc
        )
        RServer.get_model_wrapper().create_model(metadata_4_save)

    def create_metadata_4_save(self, epoch, weight_path, train_acc, val_acc):
        metadata_4_save = {
            "class_name": self.orig_metadata["class_name"],
            "nickname": self.orig_metadata["nickname"],
            "predefined": self.orig_metadata["predefined"],
            "pretrained": self.orig_metadata["pretrained"],
            "description": self.orig_metadata["description"],
            "architecture": self.orig_metadata["architecture"],
            "tags": self.orig_metadata["tags"],
            "create_time": datetime.now(),
            "code_path": self.orig_metadata["code_path"],
            "weight_path": weight_path,
            "epoch": self.orig_metadata["epoch"] + epoch + 1,
            "train_accuracy": train_acc,
            "val_accuracy": val_acc,
            "test_accuracy": None,
            "last_trained": datetime.now(),
            "last_eval_on_dev_set": datetime.now(),
            "last_eval_on_test_set": None,
        }
        return metadata_4_save

    def val(self):
        loader = self.val_loader

        correct = 0
        total = 0
        self.model.eval()

        with torch.no_grad():
            for data in self.buffer_val_sample(loader):
                images, labels = data
                images, labels = images.to(self.device), labels.to(self.device)
                outputs = self.model(images)

                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum()

        result = 1.0 * 100 * correct / total
        self.status_info["val_acc"] = float(result)
        self.update_gui()
        print("The validation accuracy is: %.3f%%" % result)
        torch.cuda.empty_cache()
        return result

    def buffer_val_sample(self, loader):
        if self.val_sample_buffer:
            return self.val_sample_buffer
        self.val_sample_buffer = []
        for _, data in enumerate(loader, 0):
            self.val_sample_buffer.append(data)
        return self.val_sample_buffer

    @staticmethod
    def return_a(a, b):
        return a

    def train(self, epoch, auto_save=True, pgd=False, merge=1):
        start_time = time.time()
        loader = self.train_loader
        criterion = torch.nn.CrossEntropyLoss()
        pgd_attack = (
            PGD(self.model, eps=0.2, alpha=2 / 255, iters=2)
            if pgd
            else Trainer.return_a
        )
        optimizer = torch.optim.SGD(
            self.model.parameters(), lr=self.learn_rate, momentum=0.9, weight_decay=5e-4
        )

        # init task
        task = RTask(TaskType.Training, epoch * len(loader))

        # Number of batches in one epoch
        iter_num_per_epoch = len(loader)

        for epoch in range(epoch):
            print("\nEpoch: %d" % (epoch + 1))
            s_epoch = time.time()

            sum_loss = 0.0
            correct = 0.0
            total = 0.0

            # Training
            self.model.train()
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
                outputs = self.model(inputs)
                loss = criterion(outputs, labels)

                if self.use_paired_train:
                    paired_outputs = self.model(paired_inputs)
                    paired_loss = criterion(paired_outputs, labels)
                    loss += paired_loss + self.paired_reg * torch.mean(
                        torch.square(torch.norm(outputs - paired_outputs))
                    )

                loss.backward()

                if i % merge == 0 and i != 0:
                    optimizer.step()
                    optimizer.zero_grad()

                sum_loss += loss.item()

                # Count the number of correct predictions and total number of predictions
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += predicted.eq(labels.data).cpu().sum()

                info_iter = i + 1 + epoch * iter_num_per_epoch
                info_loss = sum_loss / (i + 1)
                info_train_acc = 100.0 * correct / total

                self.status_info["epoch"] = epoch + 1
                self.status_info["iter"] = info_iter
                self.status_info["loss"] = info_loss
                self.status_info["train_acc"] = info_train_acc

                output_text = "[epoch:%d, iter:%d] Loss: %.03f | Acc: %.3f%% " % (
                    epoch + 1,
                    info_iter,
                    info_loss,
                    info_train_acc,
                )

                if self.use_tensorboard:
                    self.writer.add_scalar("train accuracy", info_train_acc, info_iter)
                    self.writer.add_scalar("loss", info_loss, info_iter)

                self.update_gui()

                print("\r" + output_text, flush=True, end="")

                # update task
                task_update_res = task.update()
                if not task_update_res:
                    end_time = time.time()
                    print("Time consumption:", end_time - start_time)
                    print("Training stopped!")
                    return

            print("Epoch Finish!")
            e_epoch = time.time()
            print(
                "Time consumption in training epoch:{} {}".format(
                    epoch + 1, e_epoch - s_epoch
                )
            )

            torch.cuda.empty_cache()

            s_epoch = time.time()
            val_acc = self.val()
            e_epoch = time.time()
            print(
                "Time consumption in testing epoch:{} {}".format(
                    epoch + 1, e_epoch - s_epoch
                )
            )
            torch.cuda.empty_cache()
            if val_acc > self.best_val_acc:
                if auto_save:
                    self.save_best_weights()
                self.best_val_acc = val_acc
                self.best_train_acc = info_train_acc
                self.best_epoch = epoch
            if (epoch + 1) % self.save_every == 0:
                self.save_epoch_model(epoch, info_train_acc, val_acc)

        # Save the best model
        self.save_best_model()

        # Save the last model if not saved
        if (epoch + 1) % self.save_every != 0 and self.best_epoch != epoch:
            self.save_epoch_model(epoch, info_train_acc, val_acc)

        end_time = time.time()
        print("Time consumption:", end_time - start_time)

        # Stop updating the tensorboard
        self.stop_tb_process()

    def set_tb_process(self, process):
        self.tb_process = process

    def stop_tb_process(self):
        self.tb_process.terminate()
