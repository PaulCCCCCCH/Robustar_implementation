"""
Author: Chonghan Chen (paulcccccch@gmail.com)
-----
Last Modified: Friday, 10th March 2023 5:03:19 pm
Modified By: Chonghan Chen (paulcccccch@gmail.com)
-----
"""
import traceback
from flask import request
from utils.train_utils import *
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
                'use_paired_train': True,
                'mixture': 'random_pure',
                'auto_save_model': True,
                'batch_size': 128,
                'shuffle': True,
                'learn_rate': 0.1,
                'paired_train_reg_coeff': 0.001,
                'epoch': 20,
                'num_workers': 8,
                'user_edit_buffering': False,
                'save_every': 5
              }
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
    try:
        print("Requested to training with the following configuration: ")
        json_data = request.get_json()
        configs = json_data["configs"]
        print(configs)

        # Return error message if config is invalid
        check_result = check_configs(configs)
        if check_result != 0:
            return RResponse.fail(f"Invalid Configuration!: {check_result}", 400)

        # Try to start training thread
        print("DEBUG: Training request received! Setting up training...")

        # start the training thread
        try:
            start_train(configs)
        except Exception as e:
            traceback.print_exc()
            return RResponse.fail(f"Failed to start training thread. {e}", 400)

        # Training started succesfully!
        print("Training started!")
        return RResponse.ok("Training started!")
    except Exception as e:
        traceback.print_exc()
        return RResponse.abort(500, f"Unexpected error. {e}")
