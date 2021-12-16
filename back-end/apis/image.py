import json

from objects.RServer import RServer
from flask import jsonify, redirect, send_from_directory, send_file
import os
import os.path as osp
from utils.image_utils import imageURLToPath

server = RServer.getServer()
app = server.getFlaskApp()

@app.route('/image/<split>/<image_id>')
def get_train_img(split, image_id):
    url = imageURLToPath('/'.join([split, image_id]))
    return redirect('/dataset/'+url)

# internal use only
@app.route('/dataset/<path:datasetImgPath>')
def get_dataset_img(datasetImgPath):
    datasetImgPath = datasetImgPath.replace("_mistake", "").replace("_correct", "")
    return send_file(osp.join('/', datasetImgPath).replace('\\', '/'))

@app.route('/visualize/<path:visualizeImgPath>')
def get_influence_img(visualizeImgPath):
    return send_file(osp.join('/', visualizeImgPath).replace('\\', '/'))


# TODO: Need refactor
@app.route('/dataset-info/<path:dataOriginId>')
def get_image_file(dataOriginId):
    return imageURLToPath(dataOriginId)

