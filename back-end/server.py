from torch._C import _valgrind_toggle_and_dump_stats
import torchvision.datasets as dset
import json
import os
import os.path as osp
from flask import Flask, render_template, redirect, send_from_directory, request, jsonify, Response
from objects.RServer import RServer
from objects.RDataManager import RDataManager
from objects.RAutoAnnotator import RAutoAnnotator
from utils.train import initialize_model
from utils.path_utils import to_unix

from influence import check_influence, load_influence, get_helpful_list, get_harmful_list, get_influence_list


def precheck():
    def check_num_classes_consistency():
        configs = RServer.getServerConfigs()
        data_manager = RServer.getDataManager()
        trainset = data_manager.trainset
        testset = data_manager.testset
        validationset = data_manager.validationset

        classes_num = configs["num_classes"]
        error_template = "Number of classes specified in configs.json({}) doesn't match that in dataset {}({})"
        errors = []
        if len(trainset.classes) != classes_num:
            errors.append(
                error_template.format(classes_num, "Training Set", len(trainset.classes))
            )
        if len(testset.classes) != classes_num:
            errors.append(
                error_template.format(classes_num, "Test Set", len(trainset.classes))
            )
        if len(validationset.classes) != classes_num:
            errors.append(
                error_template.format(classes_num, "Validation Set", len(trainset.classes))
            )
        assert len(errors) == 0, "\n".join(errors)

    check_num_classes_consistency()

def start_server():
    baseDir = to_unix(osp.join('/', 'Robustar2'))
    datasetDir = to_unix(osp.join(baseDir, 'dataset'))
    ckptDir = to_unix(osp.join(baseDir, 'checkpoints'))
    dbPath = to_unix(osp.join(baseDir, 'data.db'))

    with open(osp.join(baseDir, 'configs.json')) as jsonfile:
        configs = json.load(jsonfile)

    class2labelPath = osp.join(baseDir, 'class2label.json')
    class2labelMapping = {}
    if osp.exists(class2labelPath):
        try:
            with open(class2labelPath) as jsonfile:
                class2labelMapping = json.load(jsonfile)
                print('Class to label file loaded!')
        except Exception as e:
            print('Class to label file invalid!')
            class2labelMapping = {}
    else:
        print('Class to label file not found!')

    # Create server

    # Set data manager
    server = RServer.createServer(configs=configs, baseDir=baseDir, datasetDir=datasetDir, ckptDir=ckptDir)
    dataManager = RDataManager(
        baseDir, datasetDir, dbPath,
        batch_size=configs['batch_size'], 
        shuffle=configs['shuffle'],
        num_workers=configs['num_workers'],
        image_size=configs['image_size'],
        image_padding=configs['image_padding'],
        class2label_mapping=class2labelMapping
    )
    RServer.setDataManager(dataManager)

    # Set model (used for prediction)
    model = initialize_model()
    RServer.setModel(model)

    # Set auto annotator
    # TODO: model_name and checkpoint hard-coded for now
    checkpoint_name = "u2net.pth"
    annotator = RAutoAnnotator(
        configs['device'],
        checkpoint=osp.join(baseDir, checkpoint_name),
        model_name="u2net"
    )
    RServer.setAutoAnnotator(annotator)

    # register all api routes
    RServer.registerAPIs()

    # Check file state consistency
    precheck()


if __name__ == "__main__":
    start_server()

    # Start server
    RServer.getServer().run(port='8000', host='0.0.0.0', debug=False)
