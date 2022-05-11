import os.path as osp

from flask import redirect, send_file

from objects.RResponse import RResponse
from objects.RServer import RServer
from utils.image_utils import imageURLToPath, getSplitLength, getClassStart, get_annotated_from_train, getImagePath

server = RServer.getServer()
app = server.getFlaskApp()

warning = """
    Retrieving images with image url will not be supported soon.
    Use /image/list/<split>/<start>/<end> to get full path and 
    use /dataset/<path> to get the image
"""


@app.route('/image/list/<split>/<int: start>/<int: num_per_page>')
def get_image_list(split, start, num_per_page):
    image_idx_start = num_per_page * start
    image_idx_end = num_per_page * (start + 1)
    try:
        return RResponse.ok(getImagePath(split, image_idx_start, image_idx_end))
    except Exception as e:
        return RResponse.fail('Error retrieving image paths') 

@DeprecationWarning(warning)
@app.route('/image/<split>/<image_id>')
def get_train_img(split, image_id):
    """
    Gets the train image
    ---
    tags:
      - image
    parameters:
      - name: "split"
        in: "path"
        description: "name of the split, valid values: 'train', 'annotated', ... [TBF]"
        required: true
        type: "string"
      - name: "image_id"
        in: "path"
        description: "ID of the image"
        required: true
        type: "integer"
    responses:
      200:
        description: An image, or image with given id not exist
    """
    try:
        url = imageURLToPath('/'.join([split, image_id]))
    except Exception as e:
        print(e)
        return RResponse.fail('Image with given id not exist')
    return redirect('/dataset/' + url)


@app.route('/image/get-annotated/<image_id>')
def get_annotated(image_id):
    """
    Gets corresponding paired image id, if exists
    ---
    tags:
      - image
    parameters:
      - name: "image_id"
        in: "path"
        description: "train image id"
        required: true
        type: "integer"
    responses:
      200:
        description: Returns corresponding paired image id, if exists
        schema:
          properties:
            code:
              type: integer
              example: 0
            data:
              type: string
              example: -1
            msg:
              type: string
              example: Success
    """
    annotated_idx = get_annotated_from_train(image_id)
    if annotated_idx is None:
        return RResponse.ok(-1)
    return RResponse.ok(annotated_idx)


@app.route('/image/class/<split>')
def get_class_page(split):
    """
    Gets a map of class names with the index of the first image of the class
    ---
    tags:
      - image
    parameters:
      - name: "split"
        in: "path"
        description: "name of the split"
        required: true
        type: "string"
    responses:
      200:
        description: A map of class names with the index of the first image of the class
    """
    return RResponse.ok(getClassStart(split))


@app.route('/image/<split>')
def get_split_length(split):
    """
    Gets the length of the split
    ---
    tags:
      - image
    parameters:
      - name: "split"
        in: "path"
        description: "name of the split"
        required: true
        type: "string"
    responses:
      200:
        description: The length of the split
        schema:
          properties:
            code:
              type: integer
              example: 0
            data:
              type: string
              example: 9468
            msg:
              type: string
              example: Success
    """
    return RResponse.ok(getSplitLength(split))


@app.route('/dataset/<path:dataset_img_path>')
def get_dataset_img(dataset_img_path):
    normal_path = osp.join('/', dataset_img_path).replace('\\', '/')
    if osp.exists(normal_path):
        return send_file(normal_path)
    else:
        return RResponse.fail()

@app.route('/visualize/<path:visualize_img_path>')
def get_influence_img(visualize_img_path):
    return send_file(osp.join('/', visualize_img_path).replace('\\', '/'))
