import json
from objects.RServer import RServer
from flask import jsonify, redirect, send_from_directory, send_file
import os
from os import path as osp
from utils.image_utils import imageIdToPath

server = RServer.getServer()
app = server.getFlaskApp()

@app.route('/train/<number>')
def get_train_img(number):
    url = imageIdToPath('train'+'/'+str(number))
    return redirect('/dataset/'+url)


@app.route('/test/<number>')
def get_test_img(number):
    url = imageIdToPath('test'+'/'+str(number))
    return redirect('/dataset/'+url)

 # 根据图片路径返回图片
@app.route('/dataset/<path:datasetImgPath>')
def get_dataset_img(datasetImgPath):
    datasetImgPath = datasetImgPath.replace(
        "_mistake", "").replace("_correct", "")
    return send_file(osp.join('/', datasetImgPath))


# TODO: Need refactor
@app.route('/dataset-info/<path:dataOriginId>')
def get_image_file(dataOriginId):
    return imageIdToPath(dataOriginId)

