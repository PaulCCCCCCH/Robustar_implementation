import os.path as osp
import mimetypes
from apis.api_configs import PARAM_NAME_IMAGE_PATH
from flask import send_file, request
from objects.RResponse import RResponse
from objects.RServer import RServer
from utils.image_utils import getClassStart, getImagePath, getNextImagePath, getSplitLength, getImgData
from utils.path_utils import to_unix

server = RServer.getServer()
app = server.getFlaskBluePrint()
dataManager = server.getDataManager()



@app.route('/image/list/<split>/<int:start>/<int:num_per_page>')
def get_image_list(split, start, num_per_page):
    image_idx_start = num_per_page * start
    image_idx_end = num_per_page * (start + 1)

    try:
        ls_image_path = getImagePath(split, image_idx_start, image_idx_end)
        ls_image_data = [getImgData(image_path) for image_path in ls_image_path]
        if len(ls_image_path) == 0:
            return RResponse.fail('Error retrieving image paths - cannot get image idx [{}, {})'
                                  .format(image_idx_start, image_idx_end))
    except Exception as e:
        return RResponse.fail('Error retrieving image paths - {}'.format(str(e)))

    ls_image_path_data = list(zip(ls_image_path, ls_image_data))

    return RResponse.ok(ls_image_path_data)



    if osp.exists(normal_path):
        if normal_path in datasetFileBuffer:
            image_data = datasetFileBuffer[normal_path]
        else:
            with open(normal_path, "rb") as image_file:
                image_base64 = base64.b64encode(image_file.read()).decode()
            image_mime = mimetypes.guess_type(normal_path)[0]

            image_data = 'data:' + image_mime + ";base64," + image_base64

            datasetFileQueue.append(normal_path)
            if len(datasetFileQueue) > datasetFileQueueLen:
                temp_path = datasetFileQueue.popleft()
                del datasetFileBuffer[temp_path]
            datasetFileBuffer[normal_path] = image_data

        return image_data
    else:
        raise Exception


@app.route('/image/next/<split>')
def get_next_image(split):
    """
    Gets next image path given current image split and path.
    Only supports 'train', 'annotated' and 'proposed' splits.
    """
    if split not in ['train', 'annotated', 'proposed']:
        return RResponse.fail('Split {} not supported'.format(split))

    path = request.args.get(PARAM_NAME_IMAGE_PATH)
    path = to_unix(path)
    next_image_path = getNextImagePath(split, path)
    if next_image_path is None:
        return RResponse.fail('Invalid image path {}'.format(path))

    return RResponse.ok(next_image_path)

@app.route('/image/annotated/<split>')
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


@app.route('/dataset')
def get_dataset_img():
    path = request.args.get(PARAM_NAME_IMAGE_PATH)
    normal_path = to_unix(path)
    if osp.exists(normal_path):
        return send_file(normal_path)
    else:
        return RResponse.fail()


@app.route('/visualize')
def get_influence_img():
    visualize_img_path = request.args.get(PARAM_NAME_IMAGE_PATH)
    return send_file(to_unix(visualize_img_path))
