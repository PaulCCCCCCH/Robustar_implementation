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
            RServer.get_model_wrapper().acquire_model()
            with RServer.get_server().get_flask_app().app_context():
                self.trainer.start_train(
                    call_back=lambda status_dict: self.update_info(status_dict),
                    epochs=int(self.configs["epoch"]),
                    auto_save=self.configs["auto_save_model"],
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
    data_manager = RServer.get_data_manager()

    use_paired_train = configs["use_paired_train"]
    paired_train_mixture = configs["mixture"]
    image_size = data_manager.image_size
    trainset = data_manager.train_root
    testset = data_manager.test_root
    user_edit_buffering = configs["user_edit_buffering"]

    device = RServer.get_model_wrapper().device
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

    test_set = DataSet(testset, image_size, transforms)

    model = RServer.get_model_wrapper().get_current_model()

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

    os.system("tensorboard --logdir={} --port=6006".format(os.path.abspath(logdir)))


def start_train(configs):
    """
    Starts training on a new thread which calls back influence calculating.
    Returns the new thread.
    TODO: Set an 'exit flag' in thread object, and check regularly during training.
          This is the most elegant way that I can think of to signal a stop from the front end.
    """
    # Switch to the model to be trained
    model_wrapper = RServer.get_model_wrapper()
    model_name = configs["model_name"]
    model_wrapper.set_current_model(model_name)

    try:
        train_set, test_set, model, trainer = setup_training(configs)
        # Set up tensorboard log directory
        tb_dir = "runs"
        date = datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")
        if not os.path.exists(tb_dir):
            os.mkdir(tb_dir)
        run_dir = os.path.join(tb_dir, "run_{}".format(date))
        writer = SummaryWriter(run_dir)
        trainer.writer = writer
        writer.add_scalar("train accuracy", 0, 0)
        writer.add_scalar("loss", 0, 0)

        # Start the tensorboard writer as a new process
        t = multiprocessing.Process(target=start_tensorboard, args=(tb_dir,))
        t.start()
        trainer.set_tb_process(t)

        train_thread = TrainThread(trainer, configs)

        # Start training on a new thread
        train_thread.start()

    except Exception as e:
        raise e

    return train_thread


def check_configs(config):
    """
    Check the config of the server. Returns 0 if config is valid.
    Otherwise, return an error code from the following table:
    error code  |       meaning
        10      | Training set not found or not valid
        11      | Test set not found or not valid
        12      | Dev set not found or not valid
        13      | Class file not found or not valid
        14      | Weight file not found or not valid
        15      | Path for the source data set to be mirrored is not valid
        16      | User edit json file path not valid

        20      | paired train reg coeff not valid
        21      | learn rate not valid
        22      | epoch num not valid
        23      | image size not valid
        24      | thread number not valid
        25      | batch size not valid
    """
    # TODO: check the config here
    return 0
