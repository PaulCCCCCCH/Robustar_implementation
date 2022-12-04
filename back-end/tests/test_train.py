import os
import time

import torch

from test_app import app, client


# class TestTrain:
#     # Test if the model is loaded correctly at weight level
#     def test_load_model_correctness(self, client, server):
#         assert server.getModelsWeights() == {}
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
#         for name, weight in server.getModelsWeights().items():
#             # Get the model weights saved in local path
#             model_arch = server.getServerConfigs()['model_arch']
#             net_path = os.path.join(server.ckptDir, name).replace('\\', '/')
#             device = server.getServerConfigs()['device']
#             pre_trained = server.getServerConfigs()['pre_trained']
#             num_classes = server.getServerConfigs()['num_classes']
#             modelWrapper = RModelWrapper(model_arch, net_path, device, pre_trained, num_classes)
#             modelLoaded = modelWrapper.model
#             weightLoaded = modelLoaded.state_dict()
#
#             # Get the model weights saved in memory
#             weightInMem = server.getModelsWeights()[name]
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
