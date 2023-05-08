from modules.ml import DataSet, PairedDataset, Trainer
import os
from datetime import datetime
from torch.utils.tensorboard import SummaryWriter
from objects.RServer import RServer
import threading
import multiprocessing


class TrainThread(threading.Thread):
    def __init__(self, trainer, configs):
        super(TrainThread, self).__init__()
        self.trainer = trainer
        self.configs = configs

    def run(self):
        try:
            self.trainer.start_train(
                call_back=lambda status_dict: self.update_info(status_dict),
                epochs=int(self.configs["epoch"]),
                auto_save=self.configs["auto_save_model"] == "yes",
            )
        except Exception as e:
            raise e
        finally:
            RServer.get_model_wrapper().release_model()

    def update_info(self, status_dict):
        return """This is a placeholder function. If anything needs to be done
        after each iteration, put it here.
        """


def setup_training(configs):
    # Configs from training pad
    dataManager = RServer.get_data_manager()

    use_paired_train = configs["use_paired_train"]
    paired_train_mixture = configs["mixture"]
    image_size = dataManager.image_size
    trainset = dataManager.train_root
    testset = dataManager.test_root
    user_edit_buffering = configs["user_edit_buffering"]
    model_name = configs["model_name"] if configs["model_name"] else "my-model"

    # Default configs from the server
    save_dir = RServer.get_server().ckpt_dir
    device = RServer.get_server_configs()["device"]
    data_manager = RServer.get_data_manager()
    transforms = data_manager.transforms
    paired_data_path = data_manager.paired_root

    if use_paired_train:
        train_set = PairedDataset(
            trainset,
            paired_data_path,
            image_size,
            transforms,
            paired_train_mixture,
            user_edit_buffering,
        )
    else:
        train_set = DataSet(trainset, image_size, transforms)

    test_set = DataSet(testset, int(configs["image_size"]), transforms)

    # Model will be initialized with server config
    model_wrapper = RServer.get_model_wrapper()
    model = model_wrapper.model

    trainer = Trainer(
        net=model,
        trainset=train_set,
        testset=test_set,
        batch_size=int(configs["batch_size"]),
        shuffle=configs["shuffle"],
        num_workers=int(configs["num_workers"]),
        device=device,
        learn_rate=float(configs["learn_rate"]),
        auto_save=configs["auto_save_model"],
        save_every=int(configs["save_every"]),
        save_dir=save_dir,
        name=model_name,
        use_paired_train=configs["use_paired_train"],
        paired_reg=float(configs["paired_train_reg_coeff"]),
    )

    return train_set, test_set, model, trainer


def start_tensorboard(logdir):
    """
    Starts updating tensorboard.
    """

    os.system("tensorboard --logdir={}".format(os.path.abspath(logdir)))


def start_train(configs):
    """
    Starts training on a new thread which calls back influence calculating.
    Returns the new thread.
    TODO: Set an 'exit flag' in thread object, and check regularly during training.
          This is the most elegant way that I can think of to signal a stop from the front end.
    """

    print("configs:", configs)

    model_wrapper = RServer.get_model_wrapper()
    if not model_wrapper.acquire_model():
        raise Exception(
            "Cannot start training because the model is occupied by another thread"
        )

    try:
        train_set, test_set, model, trainer = setup_training(configs)
        # Set up tensorboard log directory
        date = datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")
        if not os.path.exists("runs"):
            os.mkdir("runs")
        logdir = os.path.join("runs", "run_{}".format(date))
        writer = SummaryWriter(logdir)
        trainer.writer = writer
        writer.add_scalar("train accuracy", 0, 0)
        writer.add_scalar("loss", 0, 0)

        # Start the tensorboard writer as a new process
        t = multiprocessing.Process(target=start_tensorboard, args=(logdir,))
        t.start()
        trainer.set_tb_process(t)

        train_thread = TrainThread(trainer, configs)

        # Start training on a new thread
        train_thread.start()

    except Exception as e:
        model_wrapper.release_model()
        raise e

    return train_thread
