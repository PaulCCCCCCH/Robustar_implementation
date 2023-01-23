import os.path as osp
from apis.api_configs import PARAM_NAME_IMAGE_PATH
from flask import send_file, request
from objects.RResponse import RResponse
from utils.image_utils import (
    get_class_start,
    get_image_path,
    get_next_image_path,
    get_img_Data,
    get_split_length,
    get_annotated,
    get_classified_split_length
)
from utils.path_utils import to_unix
from flask import Blueprint

image_api = Blueprint("image_api", __name__)


@image_api.route("/image/list/<split>/<int:start>/<int:num_per_page>")
def get_image_list(split, start, num_per_page):
    if num_per_page == 0:
        RResponse.abort(400, "Invalid non-positive num_per_page")

    image_idx_start = num_per_page * start
    image_idx_end = num_per_page * (start + 1)

    try:
        ls_image_path = get_image_path(split, image_idx_start, image_idx_end)
        ls_image_data = [get_img_Data(image_path) for image_path in ls_image_path]
        ls_image_path_data = list(zip(ls_image_path, ls_image_data))
        return RResponse.ok(ls_image_path_data)
    except (ValueError, NotImplementedError) as e:
        print(e)
        RResponse.abort(400, "{}".format(str(e)))
    except Exception as e:
        print(e)
        RResponse.abort(500, str(e))


@image_api.route("/image/next/<split>")
def get_next_image(split):
    """
    Gets next image path given current image split and path.
    Only supports 'train', 'annotated' and 'proposed' splits.
    """
    path = request.args.get(PARAM_NAME_IMAGE_PATH)
    path = to_unix(path)
    try:
        next_image_path = get_next_image_path(split, path)
    except NotImplementedError as e:
        RResponse.abort(400, str(e))

    if next_image_path is None:
        RResponse.abort(400, "Invalid image path {}".format(path))

    return RResponse.ok(next_image_path)


@image_api.route("/image/annotated/<split>")
def get_annotated(split):
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
    path = request.args.get(PARAM_NAME_IMAGE_PATH)
    path = to_unix(path)
    return RResponse.ok(get_annotated(split, path))


@image_api.route("/image/class/<split>")
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
        response = get_class_start(split)
    except Exception:
        RResponse.abort(400, "Split not supported")

    return RResponse.ok(response)


@image_api.route("/image/<split>")
def api_get_split_length(split):
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
        response = get_split_length(split)
    except Exception as e:
        print(e)
        RResponse.abort(400, "Split not supported")

    return RResponse.ok(response)

@image_api.route('/image/classified/<split>')
def get_classfied_split_length(split):
    """
    Gets the length of all/correctly classified/incorrectly classified split lengt
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
      response = get_classified_split_length(split)
      print(response)
    except Exception as e:
      print(e)
      RResponse.abort(400, "Split {} not supported".format(split))
    return RResponse.ok(response)


@image_api.route("/dataset")
def get_dataset_img():
    path = request.args.get(PARAM_NAME_IMAGE_PATH)
    normal_path = to_unix(path)
    if osp.exists(normal_path):
        return send_file(normal_path)
    else:
        RResponse.abort(500, "Failed to retrieve image")


@image_api.route("/visualize")
def get_influence_img():
    visualize_img_path = request.args.get(PARAM_NAME_IMAGE_PATH)
    return send_file(to_unix(visualize_img_path))
