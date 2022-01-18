import os.path as osp

from flask import redirect, send_file

from objects.RResponse import RResponse
from objects.RServer import RServer
from utils.image_utils import imageURLToPath, getSplitLength, getClassStart

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


@app.route('/image/class/<split>')
def get_class_page(split):
    return RResponse.ok(getClassStart(split))


@app.route('/image/<split>')
def get_split_length(split):
    return RResponse.ok(getSplitLength(split))


# internal use only
@app.route('/dataset/<path:dataset_img_path>')
def get_dataset_img(dataset_img_path):
    return send_file(osp.join('/', dataset_img_path).replace('\\', '/'))


@app.route('/visualize/<path:visualize_img_path>')
def get_influence_img(visualize_img_path):
    return send_file(osp.join('/', visualize_img_path).replace('\\', '/'))


# TODO: Need refactor
@app.route('/dataset-info/<path:data_origin_id>')
def get_image_file(data_origin_id):
    return imageURLToPath(data_origin_id)
