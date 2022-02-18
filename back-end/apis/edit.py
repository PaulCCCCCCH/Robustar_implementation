from objects.RServer import RServer
from objects.RResponse import RResponse
from flask import request
from io import BytesIO
import numpy as np
from PIL import Image
import base64
from utils.image_utils import imageURLToPath, get_train_from_annotated
from utils.path_utils import get_paired_path
import os.path as osp

server = RServer.getServer()
app = server.getFlaskApp()
dataManager = server.getDataManager()

@app.route('/edit/<split>/<image_id>', methods=['POST'])
def user_edit(split, image_id):
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
    with Image.open(BytesIO(decoded)) as img:
        
        img_path = imageURLToPath('{}/{}'.format(split, image_id))

        paired_img_path = get_paired_path(img_path, dataManager.train_root, dataManager.paired_root)

        to_save = img.resize((w, h))
        to_save = to_save.convert('RGB') # image comming from canvas is RGBA

        to_save.save(paired_img_path)

        if int(image_id) in dataManager.annotatedInvBuffer:
            save_idx = dataManager.annotatedInvBuffer[int(image_id)]
        else:
            save_idx = len(dataManager.annotatedBuffer)
            dataManager.annotatedInvBuffer[int(image_id)] = save_idx
        dataManager.annotatedBuffer[save_idx] = int(image_id)

        dataManager.dump_annotated_list() # TODO: Change this to SQLite

    return RResponse.ok("Success!")


@app.route('/propose/<split>/<image_id>')
def propose_edit(split, image_id):
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

    image_url = '{}/{}'.format(split, image_id)
    proposedAnnotationBuffer = dataManager.proposedAnnotationBuffer

    if int(image_id) not in proposedAnnotationBuffer:
        image_path = imageURLToPath(image_url)
        pil_image = server.getAutoAnnotator().annotate_single(image_path, dataManager.image_size)
        # image_name = image_url.replace('.', '_').replace('/', '_').replace('\\', '_')
        proposed_image_path = get_paired_path(image_path, dataManager.train_root, dataManager.proposed_annotation_root)
        # proposed_image_path = osp.join(dataManager.proposed_annotation_root, image_name) + '.jpg'
        pil_image.save(proposed_image_path)
        proposedAnnotationBuffer.add(int(image_id))

    proposed_image_id = int(image_id)
        
    return RResponse.ok(proposed_image_id)


if __name__ == '__main__':
    print(RServer)