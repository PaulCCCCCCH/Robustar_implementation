import os.path as osp

from flask import redirect, send_file

from objects.RResponse import RResponse
from objects.RServer import RServer
from utils.image_utils import getClassStart, getImagePath, getNextImagePath, getSplitLength
from utils.path_utils import to_unix

server = RServer.getServer()
app = server.getFlaskBluePrint()
dataManager = server.getDataManager()

@app.route('/image/list/<split>/<int:start>/<int:num_per_page>')
def get_image_list(split, start, num_per_page):
    image_idx_start = num_per_page * start
    image_idx_end = num_per_page * (start + 1)
    try:
        return RResponse.ok(getImagePath(split, image_idx_start, image_idx_end))
    except Exception as e:
        return RResponse.fail('Error retrieving image paths') 
    
  
@app.route('/image/next/<split>/<path:path>')
def get_next_image(split, path):
    """
    Gets next image path given current image split and path.
    Only supports 'train', 'annotated' and 'proposed' splits.
    """
    if split not in ['train', 'annotated', 'proposed']:
        raise NotImplementedError

    path = to_unix(path)
    return RResponse.ok(getNextImagePath(split, path))
    


@app.route('/image/annotated/<split>/<path:path>')
def get_annotated(split, path):
    """
    Gets paired image path corresponding to given training path, if exists
    ---
    tags:
      - image
    parameters:
      - name: "split"
        in: "path"
        description: "image split, can be 'train', 'annotated' or 'proposed'. 
        required: true
        type: "string"
      - name: "path"
        in: "path"
        description: "`path` has to point to an image in the corresponding split."
        required: true
        type: "string"
    responses:
      200:
        description: Returns corresponding paired image path, if exists
        schema:
          properties:
            code:
              type: integer
              example: 0
            data:
              type: string
              example: ""
            msg:
              type: string
              example: Success
    """
    path = to_unix(path)
    if split == 'annotated':
        paired_path = path
    elif split == 'train':
        paired_path = dataManager.pairedset.get_paired_by_train(path)
    else:
        return RResponse.ok("")

    if paired_path is None:
        return RResponse.ok("")

    return RResponse.ok(paired_path)


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
    try:
        response = getClassStart(split)
    except Exception:
        return RResponse.fail("Split not supported")

    return RResponse.ok(response)


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
    try:
        response = getSplitLength(split)
    except Exception:
        return RResponse.fail("Split not supported")

    return RResponse.ok(response)


@app.route('/dataset/<path:dataset_img_path>')
def get_dataset_img(dataset_img_path):
    normal_path = to_unix(dataset_img_path)
    if osp.exists(normal_path):
        return send_file(normal_path)
    else:
        return RResponse.fail()


@app.route('/visualize/<path:visualize_img_path>')
def get_influence_img(visualize_img_path):
    return send_file(to_unix(visualize_img_path))
