import pickle

import torch
import torchvision

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
import modules.influence_module as ptif
from utils.image_utils import imageIdToPath


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


    if use_paired_train:
        train_set = PairedDataset(
            trainset, paired_data_path, image_size, classes_path, paired_train_mixture)
    else:
        train_set = DataSet(trainset, image_size, classes_path)

    test_set = DataSet(testset, image_size=int(
        configs['image_size']), classes_path=configs['class_path'])

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

    return RModelWrapper(model_arch, weight_to_load, device, pre_trained)


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

        # Start training on a new thread which calls back influence calculating
        train_thread = TrainThread(trainer, (update_info, int(configs['epoch']), configs['auto_save_model'] == 'yes'), calculate_influence)
        train_thread.start()

    except Exception as e:
        e.with_traceback()
        return None

    return train_thread

def calculate_influence(model):
    """
    Calculate the influence function for the model.

    args:
        model:  The trained model
    """

    TRAIN_DATA_PATH = '/Robustar2/dataset/test'
    TEST_DATA_PATH = '/Robustar2/dataset/train'
    INFLUENCES_SAVE_PATH = '/Robustar2/influence_images/influences.pkl'


    influences = {}

    transform = transforms.Compose(
        [transforms.ToTensor(),
         transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    trainset = torchvision.datasets.ImageFolder(root=TRAIN_DATA_PATH, transform=transform)
    trainloader = torch.utils.data.DataLoader(trainset, batch_size=1,shuffle=True, num_workers=2)

    testset = torchvision.datasets.ImageFolder(root=TEST_DATA_PATH, transform=transform)
    testloader = torch.utils.data.DataLoader(testset, batch_size=1, shuffle=False, num_workers=2)

    config = ptif.get_default_config()
    config['gpu'] = -1;
    config['test_sample_num'] = 0;
    config['recursion_depth'] = len(trainset);
    config['r_averaging'] = 1;
    ptif.init_logging('logfile.log')

    # max_influence_dicts is the dictionary containing the four most influential training images for each testing image
    #   e.g.    {
    #               "0": {
    #                       "523": 254.1763153076172,
    #                       "719": 221.39866638183594,
    #                       "667": 216.841064453125,
    #                       "653": 214.35723876953125
    #                      },
    #               "1":{...},
    #               ...
    #           }

    max_influence_dicts = ptif.calc_img_wise(config, model, trainloader, testloader)

    for i in range(len(testset)):
        train_img_paths = []

        testId = "test/" + i
        test_img_path = imageIdToPath(testId)

        max_influence_dict = max_influence_dicts[str(i)]
        trainIds = list(max_influence_dict.keys())

        for j in range(4):
            trainId = "train/" + trainIds[i]
            train_img_path = imageIdToPath(trainId)
            train_img_paths.append(train_img_path)

        influences[test_img_path] = train_img_paths

    with open(INFLUENCES_SAVE_PATH, "wb") as influence_file:
        pickle.dump(influences, influence_file)

class TrainThread(threading.Thread):

    def __init__(self, trainer, args, callback):
        super(TrainThread, self).__init__()
        self.trainer = trainer
        self.args = args
        self.callback = callback

    def run(self):
        call_back, epochs, auto_save = self.args
        self.trainer.start_train(call_back, epochs, auto_save)
        calculate_influence(self.trainer.net)
