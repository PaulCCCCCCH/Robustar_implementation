from apis.api_configs import PARAM_NAME_IMAGE_PATH
from objects.RServer import RServer
from objects.RResponse import RResponse
from flask import request
import base64
from utils.edit_utils import propose_edit, save_edit, start_auto_annotate
from utils.path_utils import to_unix

server = RServer.getServer()
app = server.getFlaskBluePrint()
dataManager = server.getDataManager()

@app.route('/edit/<split>', methods=['POST'])
def api_user_edit(split):
    """
    Save user's edit for an image
    ---
    tags:
      - edit
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - name: "split"
        in: "path"
        description: "name of the split, valid values are 'train' or 'annotated'"
        required: true
        type: "string"
      - name: "path"
        in: "path"
        description: "If `split` is 'train', then this is the path to the training image. If `split` is `annotated`, then it is the path to annotated image"
        required: true
        type: "integer"
      - in: "body"
        name: "body"
        description: "The edit config"
        required: true
        schema:
          properties:
            image:
              type: string
              example: the base64 encoding of the image
            image_height:
              type: integer
            image_width:
              type: integer
    responses:
      200:
        description: edit success
    """
    path = request.args.get(PARAM_NAME_IMAGE_PATH)

    # TODO: Maybe support editing other splits as well? Or not?
    if split not in ['train', 'annotated', 'proposed']:
        RResponse.abort(400, 'Split {} not supported'.format(split))

    path = to_unix(path)
    json_data = request.get_json()
    print(json_data)
    encoded_string = json_data['image'].split(',')[1]
    decoded = base64.b64decode(encoded_string)

    h = int(json_data['image_height'])
    w = int(json_data['image_width'])

    save_edit(split, path, decoded, h, w)

    return RResponse.ok("Success!")


@app.route('/edit/<split>', methods=['DELETE'])
def api_delete_edit(split):
    path = request.args.get(PARAM_NAME_IMAGE_PATH)
    dataManager.pairedset.remove_image(path)
    return RResponse.ok("Success!")

@app.route('/edit/clear', methods=['DELETE'])
def api_clear_edit():
    dataManager.pairedset.clear_images()
    return RResponse.ok("Success!")

@app.route('/propose/<split>')
def api_propose_edit(split):
    """
    Get edited image proposed by auto annotator

    TODO: This function may be called twice redundantly if front end user
    clicked on 'auto edit' while 'ProposedEditVue' component is still
    generating a proposed annotation. This needs to be fixed with some
    kind of lock.

    args: 
        split:    'train' or 'annotated'
        image_id: The index of the image within the dataset
    returns:
        proposed image path that can be placed in <img> tag with proper 
        server url as prefix
    """
    path = request.args.get(PARAM_NAME_IMAGE_PATH)

    proposed_image_path = ""
    if split not in ['annotated', 'train']:
        print("Cannot propose edit to a wrong split")
        return RResponse.ok(proposed_image_path)

    path = to_unix(path)
    proposed_image_path, _ = propose_edit(split, path)

    return RResponse.ok(proposed_image_path)


@app.route('/auto-annotate/<split>', methods=['POST'])
def api_auto_annotate(split):
    """
    """

    if split != 'train':
        return RResponse.abort(400,
            'Split {} not supported! Currently we only support editing the `train` or `annotated` splits!'.format(
                split))

    json_data = request.get_json()

    try:
        if (not str(json_data['start_idx_to_gen']).isnumeric()) \
          or (not str(json_data['end_idx_to_gen']).isnumeric()): 
            raise Exception("Bad input indices")
        start_idx_to_gen = int(json_data['start_idx_to_gen'])
        end_idx_to_gen = int(json_data['end_idx_to_gen'])
        start_auto_annotate(split, start_idx_to_gen, end_idx_to_gen)
    except Exception as e:
        RResponse.abort(500, 'Auto annotation failed: ' + str(e))

    return RResponse.ok('success')


if __name__ == '__main__':
    print(RServer)
