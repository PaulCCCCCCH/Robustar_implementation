import json
from objects.RServer import RServer
from flask import jsonify, redirect, send_from_directory
import os
from utils.image_utils import get_dataset_file
from utils.predict import convert_predict_to_string

server = RServer.getServer()
app = server.getFlaskApp()
datasetPath = server.datasetPath
dataManager = server.dataManager
predictBuffer = dataManager.predictBuffer


@app.route('/train/<number>')
def get_train_img(number):
    url = get_dataset_file('train'+'/'+str(number))
    return redirect('/dataset/train/'+url)


@app.route('/test/<number>')
def get_test_img(number):
    url = get_dataset_file('test'+'/'+str(number))
    return redirect('/dataset/test/'+url)
    


# TODO: Need refactor
@app.route('/dataset-info/<path:dataOriginId>')
def get_image_file(dataOriginId):
    get_dataset_file(dataOriginId)

###############################################
### Following functions are not working     ###
### They are only for reference             ###
###############################################

# TODO: Not implemented


# 存储模型输入到 model/model_putput***.json
@app.route('/get-correct-list/<type>')
def get_correct_list(type):
    from visualize import getPredict
    result = {}
    i = 0
    while(True):
        path = get_dataset_file(type+"/"+str(i))
        if(path == "none"):
            break
        
        datasetPath = RServer.getServer().datasetPath

        path = os.path.join(datasetPath, 'type', path)
        print(path)
        result[i] = getPredict(app.model.net, path, 224)
        i += 1
        print("current calculate", i)
    with open('model/model_output'+type+'.json', 'w') as f:
        json.dump(result, f)
    return jsonify(result)

# 返回预测结果
@app.route('/predict/<path:datasetImgPath>')
def get_predict_img(datasetImgPath):
    from visualize import visual
    if(not predictBuffer.get(datasetImgPath) is None):
        return predictBuffer[datasetImgPath]
    try:
        datasetImgPath = datasetImgPath.replace(
            "_mistake", "").replace("_correct", "")
        # img = './dataset/ten/'+datasetImgPath
        img = os.path.join(datasetPath, datasetImgPath)
        output = visual.visualize(app.model.net, img, 224)
        predictBuffer[datasetImgPath] = convert_predict_to_string(output)
    except Exception as e:
        print(e.args)
        return "0_0_0_0_0_0_0_0_0_0"
    return get_predict_img(datasetImgPath)


# 根据图片路径返回图片
@app.route('/dataset/<path:datasetImgPath>')
def get_dataset_img(datasetImgPath):
    datasetImgPath = datasetImgPath.replace(
        "_mistake", "").replace("_correct", "")
    return send_from_directory(datasetPath, datasetImgPath)

