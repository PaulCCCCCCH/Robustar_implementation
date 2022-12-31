from flask import request

from modules.visualize_module.visualize.visual import visualize
from apis.api_configs import PARAM_NAME_IMAGE_PATH
from objects.RDataManager import RDataManager
from objects.RServer import RServer
from objects.RResponse import RResponse
from utils.path_utils import to_unix, to_snake_path
from utils.predict import (
    convert_predict_to_array,
    CalcInfluenceThread,
    get_image_prediction,
)
from flask import Blueprint

predict_api = Blueprint("predict_api", __name__)

# Return prediction result
@predict_api.route("/predict/<split>")
def predict(split):
    """
    Gets the prediction path of the image specified by its split and path
    ---
    tags:
      - predict
    parameters:
      - name: "split"
        in: "path"
        description: "name of the split, valid values are 'train', 'test' or 'validation'"
        required: true
        type: "string"
      - name: "path"
        in: "path"
        description: "the path to the image to be predicted"
        required: true
        type: "string"
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
    server = RServer.getServer()
    dataManager = server.dataManager
    predictBuffer = dataManager.predictBuffer
    modelWrapper = RServer.getModelWrapper()

    # get attributes
    if split in ("train", "annotated"):
        attribute = dataManager.trainset.classes
    elif split in ("validation", "validation_correct", "validation_incorrect"):
        attribute = dataManager.validationset.classes
    elif split in ("test", "test_correct", "test_incorrect"):
        attribute = dataManager.testset.classes
    else:
        RResponse.abort(400, "Split not supported")

    # get output object
    visualize_root = dataManager.visualize_root
    image_path = request.args.get(PARAM_NAME_IMAGE_PATH)
    image_path = to_unix(image_path)

    if image_path in predictBuffer:
        output_object = predictBuffer[image_path]
    else:
        # get predict results
        try:
            modelWrapper.lock.acquire()
            output = get_image_prediction(
                modelWrapper, image_path, dataManager.image_size, argmax=False
            )
        except Exception as e:
            RResponse.abort(400, "Invalid image path {}".format(image_path))
        finally:
            modelWrapper.lock.release()
        output_array = convert_predict_to_array(output.cpu().detach().numpy())

        # get visualize images
        image_name = to_snake_path(image_path)
        output = visualize(
            modelWrapper, image_path, dataManager.image_size, server.configs["device"]
        )
        if len(output) != 4:
            RResponse.abort(
                500, "[Unexpected] Invalid number of predict visualize figures"
            )

        predict_fig_routes = []
        for i, fig in enumerate(output):
            predict_fig_route = "{}/{}_{}.png".format(
                visualize_root, image_name, str(i)
            )
            fig.savefig(predict_fig_route)
            predict_fig_routes.append(predict_fig_route)

        output_object = [output_array, predict_fig_routes]
        predictBuffer[image_path] = output_object

    # combine and return
    return_value = [attribute, output_object[0], output_object[1]]
    # print(return_value)

    return RResponse.ok(return_value)


@predict_api.route("/influence/<split>")
def get_influence(split):
    """
     Gets the influence for an image specified by its id
    ---
    tags:
      - predict
    parameters:
      - name: "split"
        in: "path"
        description: "name of the split, valid values are 'train', 'test' or 'validation'"
        required: true
        type: "string"
      - name: "image_path"
        in: "path"
        description: "the path to the image"
        required: true
        type: "string"
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
    dataManager = RServer.getDataManager()
    influence_dict = dataManager.get_influence_dict()
    image_path = request.args.get(PARAM_NAME_IMAGE_PATH)
    image_path = to_unix(image_path)
    if image_path not in influence_dict:
        RResponse.abort(
            400, "Image is not found or influence for that image is not calculated"
        )
    return RResponse.ok(influence_dict[image_path], "Success")


@predict_api.route("/influence", methods=["POST"])
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
                test_sample_start_idx: 2,
                test_sample_end_idx: 5,
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
    configs = json_data["configs"]
    calcInfluenceThread = CalcInfluenceThread(
        RServer.getModelWrapper(),
        RServer.getDataManager(),
        start_idx=int(configs["test_sample_start_idx"]),
        end_idx=int(configs["test_sample_end_idx"]),
        r_averaging=int(configs["r_averaging"]),
    )
    calcInfluenceThread.start()
    return RResponse.ok({}, "Influence calculation started!")
