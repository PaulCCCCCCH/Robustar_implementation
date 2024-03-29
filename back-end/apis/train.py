'''
Author: Chonghan Chen (paulcccccch@gmail.com)
-----
Last Modified: Friday, 10th March 2023 5:03:19 pm
Modified By: Chonghan Chen (paulcccccch@gmail.com)
-----
'''
from flask import request
from utils.train import start_train
from objects.RResponse import RResponse
from objects.RTask import RTask, TaskType
from flask import Blueprint

train_api = Blueprint("train_api", __name__)


@train_api.route("/train/stop", methods=["GET"])
def stop_training():
    """
    Stops the training thread
    ---
    tags:
      - train
    produces:
      - "application/json"
    responses:
      200:
        description: Training stopped or training cannot be stopped
        schema:
          properties:
            code:
              type: integer
              example: 0
            data:
              type: string
              example: Training stopped!
            msg:
              type: string
              example: Success
    """
    try:
        RTask.exit_tasks_of_type(TaskType.Training)
    except:
        RResponse.abort(500, "Failed to stop training", -1)

    return RResponse.ok("Training stopped!")


@train_api.route("/train", methods=["POST"])
def start_training():
    """
    Takes in a training config and start the training thread
    The server will check the configs before start training
    ---
    tags:
      - train
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - in: "body"
        name: "body"
        description: "The training config"
        required: true
        schema:
          properties:
            configs:
              type: object
              example: {
                'model_name': 'my-test-model',
                'weight': '',
                'train_path': '/Robustar2/dataset/train',
                'test_path': '/Robustar2/dataset/test',
                'class_path': './model/cifar-class.txt',
                'use_paired_train': True,
                'mixture': 'random_pure',
                'auto_save_model': True,
                'batch_size': '128',
                'shuffle': True,
                'learn_rate': 0.1,
                'pgd': 'no PGD',
                'paired_train_reg_coeff': 0.001,
                'image_size': 32,
                'epoch': 20,
                'thread': 8,
                'pretrain': False,
                'user_edit_buffering': False,
                'save_every': 5
              }
            info:
              type: string
              example: placeholder
    responses:
      200:
        description: Training started or training cannot be started
        schema:
          properties:
            code:
              type: integer
              example: 0
            data:
              type: string
              example: Training started!
            msg:
              type: string
              example: Success
    """

    print("Requested to training with the following configuration: ")
    json_data = request.get_json()
    print(json_data)
    configs = json_data["configs"]
    print(configs)

    # Return error message if config is invalid
    check_result = check_configs(configs)
    if check_result != 0:
        RResponse.abort(400, "Invalid Configuration!", check_result)

    # Try to start training thread
    print("DEBUG: Training request received! Setting up training...")

    # start the training thread
    train_thread = None
    try:
        train_thread = start_train(configs)
    except Exception as e:
        print(e)
        RResponse.abort(500, f"Failed to start training thread. ({e})", -1)

    # Return error if training cannot be started
    if not train_thread:
        print(e)
        RResponse.abort(500, "Failed to start training thread", -1)

    # Training started succesfully!
    print("Training started!")
    return RResponse.ok("Training started!")


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
