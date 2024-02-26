import os
import time
import pytest
import torch
from .utils import dummy_api_upload_dummy_model, must_succeed


def build_dummy_training_config(nickname, model_id):
    configs = {
        "model_id": model_id,
        "nickname": nickname,
        "model_name": 'simple-classifier',
        "use_paired_train": False,
        "mixture": 'random_pure',
        "auto_save_model": False,
        "batch_size": 128,
        "shuffle": True,
        "learn_rate": 0.1,
        "paired_train_reg_coeff": 0.001,
        "epoch": 3,
        "num_workers": 8,
        "user_edit_buffering": False,
        "save_every": 5,
        "use_tensorboard": False
    }

    return configs


def poll_for_api_call(api_call, task_name = "Unnamed API Call", max_retry = 10, retry_interval_secs = 5):
    """
    api_call should be a function that returns None on failure

    Must succeed, i.e., Returns an API call response on success, otherwise fail the test case.
    """

    curr_retry = 0
    while True:
        time.sleep(retry_interval_secs)
        print(f"Waiting for {task_name} to finish")

        res = api_call()

        if res is not None:
            return res

        curr_retry += 1
        if curr_retry >= max_retry:
            print(f"{task_name} failed after retrying {max_retry} times")
            return None


def poll_for_training_start(client, max_retry = 10, retry_interval_secs = 5):

    def check_task_creation():
        # API call to check for task has to succeed
        resp = client.get("/task")
        assert resp.status_code == 200
        data = resp.get_json().get('data')
        assert data is not None

        if len(data) == 0:
            return None

        return data[0]

    task = poll_for_api_call(check_task_creation, "GetTaskList - Expect length > 0", max_retry, retry_interval_secs)
    assert task is not None, "Training task never seen in task center"

    def check_task_start():
        resp = client.get(f"/task/{task['tid']}")
        assert resp.status_code == 200

        if resp.get_json()['data']['remaining_time'] != float("inf"):
            return True
        return None

    started = poll_for_api_call(check_task_start, "GetTask - Expect non-infinite remaining time", max_retry, retry_interval_secs)
    assert started, "Training thread never started"


def poll_for_task_stop(client, max_retry = 10, retry_interval_secs = 5):
    def check_task_list_empty():
        resp = client.get(f"/task")
        assert resp.status_code == 200

        if len(resp.get_json()['data']) == 0:
            return True
        return None

    poll_for_api_call(check_task_list_empty, "GetTaskList - Expect length = 0", max_retry, retry_interval_secs)


class TestTrain:
    def test_train_start_stop(self, client, reset_db):
        model_name = "test-train-start-stop-1"

        # Upload a new empty model 
        resp = must_succeed(lambda: dummy_api_upload_dummy_model(client))
        model_id = resp.get_json()['data']['id']
        assert model_id, f"Seeing invalid model ID '{model_id}' in uploaded model."

        # Start Training
        configs = build_dummy_training_config(model_name, model_id)
        resp = client.post("/train", json={"configs": configs})
        assert resp.status_code == 200, f"Failed to start training. {resp.get_json().get('detail')}"

        # Wait for training to start
        poll_for_training_start(client)

        # Stop Training
        resp = client.get("/train/stop")
        assert resp.status_code == 200

        # Wait for all tasks to stop
        poll_for_task_stop(client)

# class TestTrain:
#     # Test if the model is loaded correctly at weight level
#     def test_load_model_correctness(self, client, server):
#         assert server.get_model_weights() == {}
#
#         data = {
#             'info': 'placeholder',
#             'configs': {
#                 'model_name': 'my-test-model',
#                 'weight': '',
#                 'train_path': '/Robustar2/dataset/train-10',
#                 'test_path': '/Robustar2/dataset/test-10',
#                 'class_path': './model/cifar-class.txt',
#                 'port': '8000',
#                 'save_dir': '/Robustar2/checkpoints',
#                 'use_paired_train': False,
#                 'mixture': 'random_pure',
#                 'paired_data_path': '/Robustar2/dataset/paired',
#                 'auto_save_model': True,
#                 'batch_size': '27',
#                 'shuffle': True,
#                 'learn_rate': 0.003,
#                 'pgd': 'no PGD',
#                 'paired_train_reg_coeff': 0.001,
#                 'image_size': 32,
#                 'epoch': 5,
#                 'thread': 4,
#                 'pretrain': False,
#                 'user_edit_buffering': False,
#                 'save_every': 1
#             }
#         }
#
#         rv = client.post("/train", json=data).get_json()
#         assert rv['code'] == 0
#         assert rv['data'] == 'Training started!'
#         assert rv['msg'] == 'Success'
#
#         # Wait for the training
#         time.sleep(30)
#
#         # Compare model weights saved in local path and in memory
#         for name, weight in server.get_model_weights().items():
#             # Get the model weights saved in local path
#             model_arch = server.get_server_configs()['model_arch']
#             net_path = os.path.join(server.ckpt_dir, name).replace('\\', '/')
#             device = server.get_server_configs()['device']
#             pre_trained = server.get_server_configs()['pre_trained']
#             num_classes = server.get_server_configs()['num_classes']
#             model_wrapper = RModelWrapper(model_arch, net_path, device, pre_trained, num_classes)
#             modelLoaded = model_wrapper.model
#             weightLoaded = modelLoaded.state_dict()
#
#             # Get the model weights saved in memory
#             weightInMem = server.get_model_weights()[name]
#
#             # Compare each item in them
#             for key_item_1, key_item_2 in zip(weightLoaded.items(), weightInMem.items()):
#                 assert torch.equal(key_item_1[1], key_item_2[1])
#
#     # Test whether training works correctly
#     def test_train_model(self, client, server):
#         # Test non-paired training
#         data = {
#             'info': 'placeholder',
#             'configs': {
#                 'model_name': 'test-regular-training',
#                 'weight': '',
#                 'train_path': '/Robustar2/dataset/train-10',
#                 'test_path': '/Robustar2/dataset/test-10',
#                 'class_path': './model/cifar-class.txt',
#                 'port': '8000',
#                 'save_dir': '/Robustar2/checkpoints',
#                 'use_paired_train': False,
#                 'mixture': 'random_pure',
#                 'paired_data_path': '/Robustar2/dataset/paired',
#                 'auto_save_model': True,
#                 'batch_size': '27',
#                 'shuffle': True,
#                 'learn_rate': 0.003,
#                 'pgd': 'no PGD',
#                 'paired_train_reg_coeff': 0.001,
#                 'image_size': 32,
#                 'epoch': 5,
#                 'thread': 4,
#                 'pretrain': False,
#                 'user_edit_buffering': False,
#                 'save_every': 1
#             }
#         }
#
#         rv = client.post("/train", json=data).get_json()
#         assert rv['code'] == 0
#         assert rv['data'] == 'Training started!'
#         assert rv['msg'] == 'Success'
#
#         # Wait for the training
#         time.sleep(30)
#
#         # Check the improvement of accuracy
#         assert server.getTrainedAcc() > server.getInitAcc()
#
#         # Test paired training
#         data = {
#             'info': 'placeholder',
#             'configs': {
#                 'model_name': 'test-regular-training',
#                 'weight': '',
#                 'train_path': '/Robustar2/dataset/train-10',
#                 'test_path': '/Robustar2/dataset/test-10',
#                 'class_path': './model/cifar-class.txt',
#                 'port': '8000',
#                 'save_dir': '/Robustar2/checkpoints',
#                 'use_paired_train': True,
#                 'mixture': 'random_pure',
#                 'paired_data_path': '/Robustar2/dataset/paired-10',
#                 'auto_save_model': True,
#                 'batch_size': '27',
#                 'shuffle': True,
#                 'learn_rate': 0.003,
#                 'pgd': 'no PGD',
#                 'paired_train_reg_coeff': 0.001,
#                 'image_size': 32,
#                 'epoch': 5,
#                 'thread': 4,
#                 'pretrain': False,
#                 'user_edit_buffering': False,
#                 'save_every': 1
#             }
#         }
#
#         rv = client.post("/train", json=data).get_json()
#         assert rv['code'] == 0
#         assert rv['data'] == 'Training started!'
#         assert rv['msg'] == 'Success'
#
#         # Wait for the training
#         time.sleep(30)
#
#         # Check the improvement of accuracy
#         assert server.getTrainedAcc() > server.getInitAcc()
