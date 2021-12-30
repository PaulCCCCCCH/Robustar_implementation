from ml import DataSet, PairedDataset, Trainer
import sys
import math
import time
import os
from datetime import datetime
from torch.utils.tensorboard import SummaryWriter
import torchvision.transforms as transforms
from objects.RServer import RServer
from objects.RModelWrapper import RModelWrapper
import threading

def ml_initialize(configs):

    # Configs from training pad
    batch_size = int(configs['batch_size'])
    learn_rate = float(configs['learn_rate'])
    num_workers = int(configs['thread'])
    shuffle = True if configs['shuffle'] == "yes" else False
    save_dir = configs['save_dir'] if configs['save_dir'] else '/temp_path'
    use_paired_train = True if configs['use_paired_train'] == 'yes' else False
    paired_data_path = configs['paired_data_path']
    paired_train_reg_coeff = float(configs['paired_train_reg_coeff'])
    paired_train_mixture = configs['mixture']
    image_size = int(configs['image_size'])
    classes_path = configs['class_path']
    trainset = configs['train_path']
    testset = configs['test_path']
    device = RServer.getServerConfigs()['device']

    dataManager = RServer.getDataManager()
    transforms = dataManager.transforms

    if use_paired_train:
        train_set = PairedDataset(
            trainset, paired_data_path, image_size, transforms, classes_path, paired_train_mixture)
    else:
        train_set = DataSet(trainset, image_size, transforms, classes_path)

    test_set = DataSet(testset, int(
        configs['image_size']), transforms, classes_path=configs['class_path'])

    modelwrapper = initialize_model() # Model will be initialized with server config
    model = modelwrapper.model

    trainer = Trainer(model, train_set, test_set, batch_size,
                      shuffle, num_workers, device, learn_rate, True,
                      save_dir, modelwrapper.modelwork_type,
                      use_paired_train=use_paired_train,
                      paired_reg=paired_train_reg_coeff)

    return train_set, test_set, model, trainer



def initialize_model():
    # Configs given at server boot time
    server_configs = RServer.getServerConfigs()
    model_arch = server_configs['model_arch']
    weight_to_load = server_configs['weight_to_load']
    device = server_configs['device']
    pre_trained = server_configs['pre_trained']
    num_classes = server_configs['num_classes']

    return RModelWrapper(model_arch, weight_to_load, device, pre_trained, num_classes)


def update_info(status_dict):
    return """This is a placeholder function. If anything needs to be done
    after each iteration, put it here.
    """

def start_train(configs):
    """
    Starts training on a new thread which calls back influence calculating.
    Returns the new thread.
    TODO: Set an 'exit flag' in thread object, and check regularly during training.
          This is the most elegant way that I can think of to signal a stop from the front end.
    """

    print("configs:", configs)

    train_set, test_set, model, trainer = ml_initialize(configs)

    iter_per_epoch = math.ceil(1.0*len(train_set)/int(configs['batch_size']))
    start_train_time = time.time()

    try:

        # Set up tensorboard log directory
        date = datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")
        if not os.path.exists("runs"):
            os.mkdir("runs")
        logdir = os.path.join('runs', 'run_{}'.format(date))
        writer = SummaryWriter(logdir)
        trainer.writer = writer

        writer.add_scalar(
            'train accuracy', 0, 0)
        writer.add_scalar('loss', 0, 0)

        # import threading
        # Start the tensorboard writer as a new process

        def startTB():
            os.system('tensorboard --logdir={}'.format(os.path.abspath(logdir)))
        t = threading.Thread(target=startTB)
        t.start()

        # os.system('tensorboard --logdir={} &'.format(logdir))
        # Start training on a new thread
        # train_thread = threading.Thread(target=trainer.start_train, args=(
        #     update_info, int(configs['epoch']), configs['auto_save_model'] == 'yes'))
        # train_thread.start()

        # Start training on a new thread
        train_thread = TrainThread(trainer, (update_info, int(configs['epoch']), configs['auto_save_model'] == 'yes'))
        train_thread.start()

    except Exception as e:
        e.with_traceback()
        return None

    return train_thread


class TrainThread(threading.Thread):

    def __init__(self, trainer, args, callback=None):
        super(TrainThread, self).__init__()
        self.trainer = trainer
        self.args = args
        self.callback = callback

    def run(self):
        call_back, epochs, auto_save = self.args
        self.trainer.start_train(call_back, epochs, auto_save)
    
    def stop(self):
        print("Setting trainer stop flag...")
        self.trainer.stop = True