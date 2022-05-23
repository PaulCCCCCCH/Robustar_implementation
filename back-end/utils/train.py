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
import multiprocessing

def ml_initialize(configs):

    # Configs from training pad
    use_paired_train = configs['use_paired_train']
    paired_data_path = configs['paired_data_path']
    paired_train_mixture = configs['mixture']
    image_size = int(configs['image_size'])
    classes_path = configs['class_path']
    trainset = configs['train_path']
    testset = configs['test_path']
    user_edit_buffering = configs['user_edit_buffering']
    save_dir = configs['save_dir'] if configs['save_dir'] else '/temp_path'

    model_name = configs['model_name'] if configs['model_name'] else "my-model"
    device = RServer.getServerConfigs()['device']

    dataManager = RServer.getDataManager()
    transforms = dataManager.transforms

    if use_paired_train:
        train_set = PairedDataset(
            trainset, paired_data_path, image_size, transforms, 
            classes_path, paired_train_mixture, user_edit_buffering)
    else:
        train_set = DataSet(trainset, image_size, transforms, classes_path)

    test_set = DataSet(testset, int(
        configs['image_size']), transforms, classes_path=configs['class_path'])

    # modelwrapper = initialize_model() # Model will be initialized with server config
    modelwrapper = RServer.getModelWrapper()
    model = modelwrapper.model

    trainer = Trainer(
        net=model,
        trainset=train_set,
        testset=test_set,
        batch_size=int(configs['batch_size']),
        shuffle=configs['shuffle'],
        num_workers=int(configs['thread']),
        device=device,
        learn_rate=float(configs['learn_rate']),
        auto_save=configs['auto_save_model'],
        save_every=int(configs['save_every']),
        save_dir=save_dir,
        name=model_name,
        use_paired_train=configs['use_paired_train'],
        paired_reg=float(configs['paired_train_reg_coeff'])
    )

    return train_set, test_set, model, trainer



def initialize_model():
    # Configs given at server boot time
    server_configs = RServer.getServerConfigs()
    model_arch = server_configs['model_arch']
    weight_to_load = server_configs['weight_to_load']
    device = server_configs['device']
    pre_trained = server_configs['pre_trained']
    num_classes = server_configs['num_classes']

    net_path = os.path.join(RServer.getServer().ckptDir, weight_to_load).replace('\\', '/')

    return RModelWrapper(model_arch, net_path, device, pre_trained, num_classes)


def update_info(status_dict):
    return """This is a placeholder function. If anything needs to be done
    after each iteration, put it here.
    """


def startTB(logdir):
    """
    Starts updating tensorboard.
    """

    os.system('tensorboard --logdir={}'.format(os.path.abspath(logdir)))


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
        writer.add_scalar('train accuracy', 0, 0)
        writer.add_scalar('loss', 0, 0)

        # Start the tensorboard writer as a new process
        t = multiprocessing.Process(target=startTB, args=(logdir,))
        t.start()
        trainer.set_tb_process(t)

        # Start training on a new thread
        train_thread = threading.Thread(target=trainer.start_train, args=(
            update_info, int(configs['epoch']), configs['auto_save_model'] == 'yes'))
        train_thread.start()

    except Exception as e:
        e.with_traceback()
        return None

    return train_thread