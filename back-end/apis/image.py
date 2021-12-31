import json

from objects.RServer import RServer
from objects.RResponse import RResponse
from flask import jsonify, redirect, send_from_directory, send_file
import os
import os.path as osp
from utils.image_utils import imageURLToPath, getSplitLength

server = RServer.getServer()
app = server.getFlaskApp()

@app.route('/image/<split>/<image_id>')
def get_train_img(split, image_id):
    try:
        url = imageURLToPath('/'.join([split, image_id]))
    except Exception as e:
        print(e)
        return RResponse.fail('Image with given id not exist')
    return redirect('/dataset/' + url)


@app.route('/image/<split>')
def get_split_length(split):
    return RResponse.ok(getSplitLength(split))


# internal use only
@app.route('/dataset/<path:datasetImgPath>')
def get_dataset_img(datasetImgPath):
    return send_file(osp.join('/', datasetImgPath).replace('\\', '/'))

@app.route('/visualize/<path:visualizeImgPath>')
def get_influence_img(visualizeImgPath):
    return send_file(osp.join('/', visualizeImgPath).replace('\\', '/'))


# TODO: Need refactor
@app.route('/dataset-info/<path:dataOriginId>')
def get_image_file(dataOriginId):
    return imageURLToPath(dataOriginId)

