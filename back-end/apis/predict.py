from numpy.lib.polynomial import roots
import torchvision
from matplotlib import pyplot as plt
from flask import request

from modules.visualize_module.visualize.visual import visualize
from objects.RDataManager import RDataManager
from objects.RServer import RServer
from objects.RResponse import RResponse
from flask import jsonify
from utils.image_utils import imageURLToPath
from os import path as osp
from utils.predict import convert_predict_to_array, CalcInfluenceThread
from utils.image_utils import imageURLToPath
import json
from utils.predict import get_image_prediction

app = RServer.getServer().getFlaskApp()
server = RServer.getServer()
dataManager = server.dataManager
predictBuffer = dataManager.predictBuffer
modelWrapper = RServer.getModelWrapper()


# Return prediction result
@app.route('/predict/<split>/<image_id>')
def predict(split, image_id):
    """
    Get the prediction path of the image specified by its id.

    args: 
        split:    'train', 'test' or 'dev'
        image_id: The index of the image within the dataset
    returns:
        [attribute, output_array, predict_fig_routes]
    """

    # e.g.  train/10, test/300
    imageURL = "{}/{}".format(split, image_id)
    visualize_root = dataManager.visualize_root

    if imageURL in predictBuffer:
        output_object = predictBuffer[imageURL]
    else:
        # get output array from prediction
        datasetImgPath = imageURLToPath(imageURL)

        # try:
        imgPath = osp.join(server.baseDir, datasetImgPath).replace('\\', '/')

        output = get_image_prediction(modelWrapper, imgPath, dataManager.image_size, argmax=False)

        output_array = convert_predict_to_array(output.cpu().detach().numpy())

        # get visualize images
        image_name = imageURL.replace('.', '_').replace('/', '_').replace('\\', '_')

        model = modelWrapper.model

        output = visualize(model, imgPath, dataManager.image_size, server.configs['device'])
        if len(output) != 4:
            raise ValueError("Invalid number of predict visualize figures. Please check.")

        predict_fig_routes = []

        for i, fig in enumerate(output):
            predict_fig_route = "{}/{}_{}.png".format(visualize_root, image_name, str(i))
            fig.savefig(predict_fig_route)
            predict_fig_routes.append(predict_fig_route)

        predictBuffer[imageURL] = [output_array, predict_fig_routes]
        output_object = [output_array, predict_fig_routes]

    # get attributes
    if split == "train":
        attribute = dataManager.trainset.classes
    elif split in ("validation", "validation_correct", "validation_incorrect"):
        attribute = dataManager.validationset.classes
    elif split in ("test", "test_correct", "test_incorrect"):
        attribute = dataManager.testset.classes
    else:
        raise ValueError("Wrong split. Please check.")

    # combine and return
    return_value = [attribute, output_object[0], output_object[1]]
    # print(return_value)

    # TODO: Design a good return format here!
    return RResponse.ok(return_value)

    # except Exception as e:
    #     print(e.args)
    #     print(e)
    #     # TODO: And design a good error return as well
    #     return "0_0_0_0_0_0_0_0_0_0"


@app.route('/influence/<split>/<image_id>')
def get_influence(split, image_id):
    """
    Get the influence for an image specified by image_url
    """
    influence_dict = dataManager.get_influence_dict()
    target_img_path = imageURLToPath('{}/{}'.format(split, image_id))  
    if target_img_path in influence_dict:
        return RResponse.ok(influence_dict[target_img_path], 'Success')
    return RResponse.fail('Image is not found or influence for that image is not calculated')


@app.route('/influence', methods=['POST'])
def calculate_influence():
    """
    Calculates the influence for the test set.
    example request body:
        {
            "configs": {
                "test_sample_num": 2, // number of test samples per class for which we calculate influence 
                "r_averaging": 10 
            }
        }

    """
    json_data = request.get_json()
    configs = json_data['configs']
    calcInfluenceThread = CalcInfluenceThread(
        modelWrapper, 
        dataManager, 
        test_sample_num=int(configs['test_sample_num']),
        r_averaging=int(configs['r_averaging'])
    )
    calcInfluenceThread.start()
    return RResponse.ok({}, "Influence calculation started!")