from ml import DataSet, PairedDataset, Model, Trainer
import sys
import math
import time
import os
from datetime import datetime
from torch.utils.tensorboard import SummaryWriter


def ml_initialize(configs):

    # 这里用来分类正确和错误的图像
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

    if use_paired_train:
        train_set = PairedDataset(
            trainset, paired_data_path, image_size, classes_path, paired_train_mixture)
    else:
        train_set = DataSet(trainset, image_size, classes_path)

    test_set = DataSet(testset, image_size=int(
        configs['image_size']), classes_path=configs['class_path'])

    model = Model(configs['model'], configs['weight'],
                  configs['device'], configs['pretrain'])

    trainer = Trainer(model.net, train_set, test_set, batch_size,
                      shuffle, num_workers, configs['device'], learn_rate, True,
                      save_dir, model.network_type,
                      use_paired_train=use_paired_train,
                      paired_reg=paired_train_reg_coeff)

    return train_set, test_set, model, trainer


def update_info(status_dict):
    return """This is a placeholder function. If anything needs to be done
    after each iteration, put it here.
    """


def start_train(configs):
    """
    Starts training on a new thread.
    Returns the new thread.
    TODO: Set an 'exit flag' in thread object, and check regularly during training.
          This is the most elegant way that I can think of to signal a stop from the front end.
    """

    from server import app, get_correct
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

        import threading
        # Start the tensorboard writer as a new process

        def startTB():
            os.system('tensorboard --logdir={}'.format(os.path.abspath(logdir)))
        t = threading.Thread(target=startTB)
        t.start()

        # os.system('tensorboard --logdir={} &'.format(logdir))

        # Start training on a new thread
        train_thread = threading.Thread(target=trainer.start_train, args=(
            update_info, int(configs['epoch']), configs['auto_save_model'] == 'yes'))
        train_thread.start()

    except Exception as e:
        return None

    return train_thread
