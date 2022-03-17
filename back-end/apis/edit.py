import shutil
from objects.RServer import RServer
from objects.RResponse import RResponse
from flask import request
import base64
from utils.image_utils import get_train_from_annotated, get_annotated_from_train, imageSplitIdToPath, copyImage
from utils.edit_utils import propose_edit, save_edit, start_auto_annotate
from utils.path_utils import get_paired_path

server = RServer.getServer()
app = server.getFlaskApp()
dataManager = server.getDataManager()

@app.route('/edit/<split>/<image_id>', methods=['POST'])
def api_user_edit(split, image_id):
    """
    Edits the width and size of the image
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
      - name: "image_id"
        in: "path"
        description: "ID of the image"
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
    # TODO: Maybe support editing other splits as well? Or not?
    if split not in ['train', 'annotated']:
        raise NotImplemented('Split {} not supported! Currently we only support editing the `train` or `annotated` splits!'.format(split))

    if split == 'annotated':
        image_id = get_train_from_annotated(image_id)
        split = 'train'

    json_data = request.get_json()
    encoded_string = json_data['image'].split(',')[1]
    decoded = base64.b64decode(encoded_string)

    h = int(json_data['image_height'])
    w = int(json_data['image_width'])

    save_edit(split, image_id, decoded, h, w)

    return RResponse.ok("Success!")


@app.route('/propose/<split>/<image_id>')
def api_propose_edit(split, image_id):
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

    proposed_image_id = ""
    if split not in ['annotated', 'train']:
        print("Cannot propose edit to a wrong split")
        return RResponse.ok(proposed_image_id)

    if split == 'annotated':
        split = 'train'
        image_id = get_train_from_annotated(image_id)

    proposed_image_id = propose_edit(split, image_id)

    return RResponse.ok(proposed_image_id)


@app.route('/auto-annotate/<split>', methods=['POST'])
def api_auto_annotate(split):
    """
    """

    if split != 'train':
        raise NotImplemented('Split {} not supported! Currently we only support editing the `train` or `annotated` splits!'.format(split))


    json_data = request.get_json()
    num_to_gen = int(json_data['num_to_gen'])
    try:
      start_auto_annotate(split, num_to_gen)
    except Exception as e:
      RResponse.fail('auto annotation failed')

    return RResponse.ok('success')
      

    

if __name__ == '__main__':
    print(RServer)