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
    Gets the prediction path of the image specified by its id
    ---
    tags:
      - predict
    parameters:
      - name: "split"
        in: "path"
        description: "name of the split, valid values are 'train', 'test' or 'dev'"
        required: true
        type: "string"
      - name: "image_id"
        in: "path"
        description: "the index of the image within the dataset"
        required: true
        type: "integer"
    responses:
      200:
        description: a list of [attribute, output_array, predict_fig_routes]
        schema:
          properties:
            code:
              type: integer
              example: 0
            data:
              type: array
              example: [
                [
                  "n01440764",
                  "n02102040",
                  "n02979186",
                  "n03000684",
                  "n03028079",
                  "n03394916",
                  "n03417042",
                  "n03425413",
                  "n03445777",
                  "n03888257"
                ],
                [
                  0.11704748123884201,
                  0.05598455294966698,
                  0.03636372834444046,
                  0.05954515188932419,
                  0.13732001185417175,
                  0.1522897481918335,
                  0.082752525806427,
                  0.041457951068878174,
                  0.2806808054447174,
                  0.03655797988176346
                ],
                [
                  "/Robustar2/visualize_images/train_0_0.png",
                  "/Robustar2/visualize_images/train_0_1.png",
                  "/Robustar2/visualize_images/train_0_2.png",
                  "/Robustar2/visualize_images/train_0_3.png"
                ]
              ]
            msg:
              type: string
              example: Success
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
        # image_name = imgPath.replace('.', '_').replace('/', '_').replace('\\', '_')
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
     Gets the influence for an image specified by its id
    ---
    tags:
      - predict
    parameters:
      - name: "split"
        in: "path"
        description: "name of the split, valid values are 'train', 'test' or 'dev'"
        required: true
        type: "string"
      - name: "image_id"
        in: "path"
        description: "the index of the image within the dataset"
        required: true
        type: "integer"
    responses:
      200:
        description: path of influence images, or influence not found or calculated
        schema:
          properties:
            code:
              type: integer
              example: -1
            data:
              type: string
              example: ""
            msg:
              type: string
              example: Image is not found or influence for that image is not calculated
    """
    influence_dict = dataManager.get_influence_dict()
    target_img_path = imageURLToPath('{}/{}'.format(split, image_id))  
    if target_img_path in influence_dict:
        return RResponse.ok(influence_dict[target_img_path], 'Success')
    return RResponse.fail('Image is not found or influence for that image is not calculated')


@app.route('/influence', methods=['POST'])
def calculate_influence():
    """
    Calculates the influence for the test set
    ---
    tags:
      - predict
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - in: "body"
        name: "body"
        description: "The configuration"
        required: true
        schema:
          properties:
            configs:
              type: object
              example: {
                test_sample_num: 2,
                r_averaging: 10
              }
    responses:
      200:
        description: Influence calculation started
        schema:
          properties:
            code:
              type: integer
              example: 0
            data:
              type: string
              example: {}
            msg:
              type: string
              example: "Influence calculation started!"
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


##########################################################
###### The following are not yet implemented #############
##########################################################

# TODO: Reference only! Not Working!
# 存储模型输入到 model/model_putput***.json
@app.route('/get-correct-list/<type>')
def get_correct_list(type):
    from visualize import getPredict
    result = {}
    i = 0
    while (True):
        path = imageURLToPath(type + "/" + str(i))
        if (path == "none"):
            break

        datasetPath = RServer.getServer().datasetPath

        path = osp.join(datasetPath, 'type', path).replace('\\', '/')
        print(path)
        result[i] = getPredict(app.model.net, path, 224)
        i += 1
        print("current calculate", i)
    with open('model/model_output' + type + '.json', 'w') as f:
        json.dump(result, f)
    return jsonify(result)


# 将编号转化为图片路径
@app.route('/predictid/<folder>/<imageid>')
def get_predict_img_from_id(folder, imageid):
    url = imageURLToPath(folder + '/' + str(imageid))
    filePath = folder + '/' + url
    return get_predict_img(filePath)


@app.route('/influence-img/<number>')
def get_random_influence_img(number):
    import random
    import math
    random_num = random.randint(1, 1000)
    random_num = math.floor(float(number) * 1000)
    url = imageURLToPath('train' + '/' + str(random_num))
    # return redirect('/dataset/train/'+url)
    return '/dataset/train/' + url


@app.route('/getinfluence/<img_id>/<helpful_num>/<harmful_num>', methods=['POST', 'GET'])
def get_influence_dic(img_id, helpful_num, harmful_num):
    result = {}
    result['success'] = 1
    if (not check_influence(img_id)):
        result['success'] = 0
        return jsonify(result)
    helpful_num = int(helpful_num)
    harmful_num = int(harmful_num)

    helpful_list = get_helpful_list(img_id)
    harmful_list = get_harmful_list(img_id)
    influence_list = get_influence_list(img_id)

    helpful_list = helpful_list[:helpful_num]
    harmful_list = harmful_list[:harmful_num]
    helpful_influence = []
    harmful_influence = []
    for i in helpful_list:
        helpful_influence.append(influence_list[i])
    for i in harmful_list:
        harmful_influence.append(influence_list[i])
    result['helpful_list'] = helpful_list
    result['harmful_list'] = harmful_list
    result['helpful_influence'] = helpful_influence
    result['harmful_influence'] = harmful_influence

    return jsonify(result)
