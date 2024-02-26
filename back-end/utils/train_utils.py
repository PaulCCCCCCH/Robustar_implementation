from modules.ml import DataSet, PairedDataset, Trainer
import os
from datetime import datetime
from torch.utils.tensorboard import SummaryWriter
from objects.RServer import RServer
from objects.RModelWrapper import RModelWrapper
import threading
import multiprocessing
import logging

logger = logging.getLogger(__name__)

class TrainThread(threading.Thread):
    def __init__(self, trainer, configs):
        super(TrainThread, self).__init__()
        self.trainer = trainer
        self.configs = configs

    def run(self):
        try:
            with RServer.get_server().get_flask_app().app_context():
                self.trainer.start_train(
                    call_back=lambda status_dict: self.update_info(status_dict),
                    epochs=self.configs["epoch"],
                    auto_save=self.configs["auto_save_model"],
                )
        except Exception as e:
            logger.exception(f"Error in training thread. {str(e)}") 
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
    train_set = data_manager.train_root
    val_set = data_manager.validation_root
    user_edit_buffering = configs["user_edit_buffering"]
    device = RServer.get_model_wrapper().device
    data_manager = RServer.get_data_manager()
    transforms = data_manager.transforms
    paired_data_path = data_manager.paired_root
    save_dir = os.path.join(
        RServer.get_server().base_dir, "generated", "models", "ckpt"
    )

    if use_paired_train:
        train_set = PairedDataset(
            train_set,
            paired_data_path,
            image_size,
            transforms,
            paired_train_mixture,
            user_edit_buffering,
        )
    else:
        train_set = DataSet(train_set, image_size, transforms)

    val_set = DataSet(val_set, image_size, transforms)

    model = RServer.get_model_wrapper().get_current_model()

    trainer = Trainer(
        model=model,
        train_set=train_set,
        val_set=val_set,
        batch_size=configs["batch_size"],
        shuffle=configs["shuffle"],
        num_workers=configs["num_workers"],
        device=device,
        learn_rate=configs["learn_rate"],
        auto_save=configs["auto_save_model"],
        save_every=configs["save_every"],
        save_dir=save_dir,
        use_paired_train=configs["use_paired_train"],
        paired_reg=configs["paired_train_reg_coeff"],
        use_tensorboard=configs["use_tensorboard"],
    )

    return train_set, val_set, model, trainer


def start_tensorboard(logdir):
    """
    Starts updating tensorboard.
    """

    os.system("tensorboard --logdir={} --port=6006".format(os.path.abspath(logdir)))


def attach_tensorboard_to_trainer(trainer):
    # Get directory names
    tb_dir = "runs"
    date = datetime.now().strftime("%Y_%m_%d_%I_%M_%S_%p")
    if not os.path.exists(tb_dir):
        os.mkdir(tb_dir)
    run_dir = os.path.join(tb_dir, "run_{}".format(date))

    # Set training metrics to be tracked
    writer = SummaryWriter(run_dir)
    writer.add_scalar("train accuracy", 0, 0)
    writer.add_scalar("loss", 0, 0)

    # Set up writer process in trainer
    trainer.writer = writer
    t = multiprocessing.Process(target=start_tensorboard, args=(tb_dir,))
    t.start()
    trainer.set_tb_process(t)



def start_train(configs):
    """
    Starts training on a new thread which calls back influence calculating.
    Returns the new thread.
    TODO: Set an 'exit flag' in thread object, and check regularly during training.
          This is the most elegant way that I can think of to signal a stop from the front end.
    """
    # Switch to the model to be trained
    model_wrapper = RServer.get_model_wrapper()
    model_id = configs.get("model_id")
    if not model_id:
        raise ValueError(f"Model with model id '{model_id}' not found.")
    model_wrapper.set_current_model(model_id)

    try:
        train_set, test_set, model, trainer = setup_training(configs)

        # Attach a tensorboard process to the trainer
        if configs.get("use_tensorboard"):
            attach_tensorboard_to_trainer(trainer)

        # Start training on a new thread
        train_thread = TrainThread(trainer, configs)
        if RServer.get_model_wrapper().acquire_model():
            train_thread.start()
        else:
            raise Exception("The model to be trained is busy.")

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
