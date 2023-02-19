#! /usr/bin/env python3

import torch
import time
import datetime
import numpy as np
import copy
import logging

from pathlib import Path
from pytorch_influence_functions.utils import save_json, display_progress

import sys, os
sys.path.append(os.path.dirname(__file__))
print(sys.path)
from torch_influence.modules import BaseObjective, LiSSAInfluenceModule

def calc_influence_single(model, module, train_loader, test_loader, test_id_num, gpu,
                          recursion_depth, r, s_test_vec=None,
                          time_logging=False):
    """Calculates the influences of all training data points on a single
    test dataset image.

    Arugments:
        model: pytorch model
        module: influence module
        train_loader: DataLoader, loads the training dataset
        test_loader: DataLoader, loads the test dataset
        test_id_num: int, id of the test sample for which to calculate the
            influence function
        gpu: int, identifies the gpu id, -1 for cpu
        recursion_depth: int, number of recursions to perform during s_test
            calculation, increases accuracy. r*recursion_depth should equal the
            training dataset size.
        r: int, number of iterations of which to take the avg.
            of the h_estimate calculation; r*recursion_depth should equal the
            training dataset size.
        s_test_vec: list of torch tensor, contains s_test vectors. If left
            empty it will also be calculated

    Returns:
        influence: list of float, influences of all training data samples
            for one test sample
        harmful: list of float, influences sorted by harmfulness
        helpful: list of float, influences sorted by helpfulness
        test_id_num: int, the number of the test dataset point
            the influence was calculated for"""

    train_dataset_size = len(train_loader.dataset)
    all_train_idxs = list(range(train_dataset_size))

    max_influence_dict = {}

    influences = module.influences(train_idxs=all_train_idxs, test_idxs=[test_id_num])
    influences = influences.tolist()

    # Populate max_influence_dict
    for i in all_train_idxs:
        max_influence_dict[i] = influences[i]
    max_influence_dict = dict(sorted(max_influence_dict.items(), key=lambda kv: abs(kv[1]), reverse=True))

    def dict_slice(adict, start, end):
        keys = adict.keys()
        dict_slice = {}
        for k in list(keys)[start:end]:
            dict_slice[k] = adict[k]
        return dict_slice
    if(i > 3):
        max_influence_dict = dict_slice(max_influence_dict, 0, 4)

    harmful = np.argsort(influences)
    helpful = harmful[::-1]

    return max_influence_dict, influences, harmful.tolist(), helpful.tolist(), test_id_num

def calc_img_wise(config, model, train_loader, test_loader):
    """Calculates the influence function one test point at a time. Calcualtes
    the `s_test` and `grad_z` values on the fly and discards them afterwards.

    Arguments:
        config: dict, contains the configuration from cli params"""
    influences_meta = copy.deepcopy(config)
    test_sample_num = config['test_sample_num']
    test_start_index = config['test_start_index']
    test_end_index = config['test_end_index']
    outdir = Path(config['outdir'])
    outdir.mkdir(exist_ok=True, parents=True)

    test_dataset_iter_len = len(test_loader.dataset)

    # Set up logging and save the metadata conf file
    logging.info(f"Running on: {test_sample_num} images per class.")
    logging.info(f"Starting at img number: {test_start_index} per class.")
    # influences_meta['test_sample_index_list'] = sample_list
    influences_meta_fn = f"influences_results_meta_{test_start_index}-" \
                         f"{test_sample_num}.json"
    influences_meta_path = outdir.joinpath(influences_meta_fn)
    save_json(influences_meta, influences_meta_path)

    influences = {}
    max_influence_dicts = {}

    # TODO: will need to be modified if we add support for other training
    # methods
    class Objective(BaseObjective):
        def train_outputs(self, model, batch):
            return model(batch[0])

        def train_loss_on_outputs(self, outputs, batch):
            outputs = torch.nn.functional.log_softmax(outputs)
            loss = torch.nn.functional.nll_loss(outputs, batch[1])
            return loss

        def train_regularization(self, params):
            return 0

        def test_loss(self, model, params, batch):
            outputs = model(batch[0])
            outputs = torch.nn.functional.log_softmax(outputs)
            loss = torch.nn.functional.nll_loss(outputs, batch[1])
            return loss

    DEVICE = torch.device("cpu" if config['gpu'] == -1 else "cuda")

    module = LiSSAInfluenceModule(
        model=model,
        objective=Objective(),
        train_loader=train_loader,
        test_loader=test_loader,
        device=DEVICE,
        damp=0.001,
        depth=config['recursion_depth'],
        repeat=config['r_averaging'],
        # TODO Add support for modifying scale
        scale=5000,
    )

    # Main loop for calculating the influence function one test sample per
    # iteration.
    for i in range(test_start_index, test_end_index):
        # If we calculate evenly per class, choose the test img indicies
        # from the sample_list instead
        start_time = time.time()
        max_influence_dict, influence, harmful, helpful, _ = calc_influence_single(
            model, module, train_loader, test_loader, test_id_num=i, gpu=config['gpu'],
            recursion_depth=config['recursion_depth'], r=config['r_averaging'])
        end_time = time.time()

        ###########
        # Different from `influence` above
        ###########
        influences[str(i)] = {}
        _, label = test_loader.dataset[i]
        influences[str(i)]['label'] = label
        influences[str(i)]['num_in_dataset'] = i
        influences[str(i)]['time_calc_influence_s'] = end_time - start_time
        influences[str(i)]['influence'] = influence
        influences[str(i)]['harmful'] = harmful[:500]
        influences[str(i)]['helpful'] = helpful[:500]

        tmp_influences_path = outdir.joinpath(f"influence_results_tmp_"
                                              f"{test_start_index}_"
                                              f"{test_sample_num}"
                                              f"_last-i_{i}.json")
        save_json(influences, tmp_influences_path)

        max_influence_dicts[str(i)] = max_influence_dict
        max_influences_path = outdir.joinpath(f"max_influences_dicts_"
                                              f"{test_start_index}_"
                                              f"{test_sample_num}"
                                              f"_last-i_{i}.json")
        save_json(max_influence_dicts, max_influences_path)

        display_progress("Test samples processed: ", i, test_end_index - test_start_index)

    logging.info(f"The results for this run are:")
    logging.info("Influences: ")
    logging.info(influence[:3])
    logging.info("Most harmful img IDs: ")
    logging.info(harmful[:3])
    logging.info("Most helpful img IDs: ")
    logging.info(helpful[:3])

    influences_path = outdir.joinpath(f"influence_results_{test_start_index}_"
                                      f"{test_sample_num}.json")
    save_json(influences, influences_path)

    return max_influence_dicts
