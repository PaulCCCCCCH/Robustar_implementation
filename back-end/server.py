import torchvision.datasets as dset
import json
import os
import re
from flask import Flask, render_template, redirect, send_from_directory, request, jsonify, Response
from train import start_train
from generate import generate_paired_data

from influence import check_influence, load_influence, get_helpful_list, get_harmful_list, get_influence_list

app = Flask(__name__, template_folder='web2')
# datasetPath = "./dataset/ten"
datasetPath = '/Robustar2/dataset'


def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


app.after_request(after_request)

# Save the given configs into a file. Not currently used.
@app.route('/post_settings', methods=['POST'])
def save_settings():
    """
    # FIXME: Reference the following code
        saveFolder = None
        if not saveFolder:
            return
        existingFiles = os.listdir(saveFolder)
        exist = False
        for fileName in existingFiles:
            if fileName.endswith('pth'):
                exist = True
                break
        if exist:
            reply = QMessageBox.question(
                self, 'Message', 'Another model is already saved here and it may be over written. Are you sure?',
                QMessageBox.Yes , QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                exist = False
        if not exist:
            self.saveToEdit.setText(saveFolder)
        """
    pass


def check_configs(config):
    """
    Check the config of the server. Returns 0 if config is valid. 
    Otherwise, return an error code from the following table:
    error code  |       meaning
        10      | Training set not found or not valid
        11      | Test set not found or not valid
        12      | Dev set not found or not valid
        13      | Class file not found or not valid
        14      | Weight file not found or not valid
        15      | Path for the source data set to be mirrored is not valid
        16      | User edit json file path not valid

        20      | paired train reg coeff not valid
        21      | learn rate not valid
        22      | epoch num not valid
        23      | image size not valid
        24      | thread number not valid
        25      | batch size not valid
    """
    # TODO: check the config here
    return 0


@app.route('/train', methods=['POST'])
def start_training():
    """
    Takes in a training config. 
    The server will check the configs before start training.
    """

    print("Requested to training with the following configuration: ")
    json_data = request.get_json()
    configs = json_data['configs']
    print(configs)

    # Return error message if config is invalid
    check_result = check_configs(configs)
    if check_result != 0:
        return {"msg": "Invalid Configuration!", "code": check_result}

    # Try to start training thread
    app.configs = configs
    print("DEBUG: Training request received! Setting up training...")

    # TODO: Save this train_thread variable somewhere. 
    # When a stop API is called, stop this thread.
    train_thread = start_train(app.configs)

    # Return error if training cannot be started
    if not train_thread:
        return {"msg": "Failed", "code": -1}

    # Training started succesfully!
    return {"msg": "Training started!", "code": 0}

@app.route('/generate', methods=['POST'])
def generate():
    print("Requested to generate paired dataset")
    json_data = request.get_json()

    # TODO: Create a new thread to do this so that it does not block the server.
    generate_paired_data(json_data['mirrored_data_path'], json_data['user_edit_path'])
    return {"msg": "Generation completed!", "code": 0}


@app.route('/main/<path:path>')
def main_route(path):
    return send_from_directory("web", path)


@app.route('/img/<filename>')
def get_file_page(filename):
    return send_from_directory("./img", filename)


@app.route('/data/chart-labels.js')
def get_chart_labels():
    return "window.labels='23333'"


@app.route('/edit', methods=['POST'])
def user_edit():
    if 'src' in request.form and 'content' in request.form:
        src = request.form.get("src")
        content = request.form.get("content")

        data = {}
        file_path = 'user-edit.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
        data[src] = content

        with open(file_path, 'w') as f:
            json.dump(data, f)

        return "success"
    return 'invalid image content'


proc = None


@app.route('/checkinfluence')
def index():
    import subprocess
    import flask
    import time

    def inner():
        global proc
        if proc == None:
            proc = subprocess.Popen(
                # call something with a lot of output so we can see it
                ['python C:/Users/donlin/Documents/GitHub/Robustar2/modules/influence_module/main1.py'],
                shell=True,
                stdout=subprocess.PIPE
            )

        for line in iter(proc.stdout.readline, ''):
            # Don't need this just shows the text streaming
            time.sleep(1)
            yield str(line.rstrip()) + '<br/>\n'

    # text/html is required for most browsers to show th$
    return flask.Response(inner(), mimetype='text/html')


@app.route('/user-edit-list', methods=['POST', 'GET'])
def get_user_edit_list():
    data = {}
    file_path = 'user-edit.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            return jsonify(list(data.keys()))
            # return str(list(data.keys()))
    return 'fail to get user edit list'


@app.route('/v1/dataset/<type>/<start>/<end>', methods=['POST', 'GET'])
def send_dataset(type, start, end):
    start, end = int(start), int(end)
    result = {}
    data = []
    ds = trainset if type == 'train' else testset
    for i in range(start, end):
        data.append(ds.samples[i])
    result['data'] = data
    result['status_code'] = 200
    return jsonify(result)


@app.route('/image/<path:imagepath>')
def send_image_api(imagepath):
    return send_from_directory('.', imagepath)


@app.route('/user-edit-id-list', methods=['POST', 'GET'])
def get_user_edit_id_list():
    from ml import ImageIdConvertor
    data = {}
    file_path = 'user-edit.json'
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
            data = list(data.keys())
            ImageIdConvertor(trainset, testset)
            # return ImageIdConvertor.dic_path_id
            for i in range(len(data)):
                # TODO: There may be a bug
                # temp = data[i].replace('/dataset', './dataset/ten')
                # temp = data[i].replace('/dataset', './dataset/imagenet')
                temp = data[i].replace('/dataset', '/Robustar2/dataset')
                data[i] = ImageIdConvertor.dic_path_id.get(temp)
            return jsonify(data)
    return 'fail to get user edit list'


@app.route('/get-edit', methods=['POST'])
def get_user_edit():
    if 'src' in request.form:
        src = request.form.get("src")
        data = {}
        file_path = 'user-edit.json'
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
        return data.get(src)
    return 'not found'

# 根据图片路径返回图片


@app.route('/dataset/<path:datasetImgPath>')
def get_dataset_img(datasetImgPath):
    datasetImgPath = datasetImgPath.replace(
        "_mistake", "").replace("_correct", "")
    return send_from_directory(datasetPath, datasetImgPath)

# 返回神经网络关注的地方


@app.route('/imgv/<random>')
def get_image_visualize(random):
    return send_from_directory("./visualize", 'img-v.png')

# 返回神经网络关注的地方


@app.route('/imgv/<num>/<random>')
def get_image_visualize_id(num, random):
    return send_from_directory("./visualize", 'img-'+str(num)+'.png')


testset = dset.ImageFolder(root=os.path.join(datasetPath, "test"))
trainset = dset.ImageFolder(root=os.path.join(datasetPath, "train"))

datasetFileBuffer = {}
predictBuffer = {}

# 用来记录正确的分类结果和错误的分类结果
CorrectBuffer, MistakeBuffer = None, None

# 获得正确分类和错误分类的编号


def get_classify_list():
    correct_list, mistake_list = [], []
    # 读取分类结果
    with open('classify.json', 'r') as f:
        results = json.load(f)
    # 处理每一条分类结果
    for i in range(len(results)):
        r = results[i]
        if r[0] == r[1]:
            correct_list.append(i)
        else:
            mistake_list.append(i)
    return correct_list, mistake_list


def get_correct(isCorrect, id):
    global CorrectBuffer, MistakeBuffer
    if CorrectBuffer is None or MistakeBuffer is None:
        CorrectBuffer, MistakeBuffer = get_classify_list()

    if isCorrect:
        img_num = CorrectBuffer[id]
    else:
        img_num = MistakeBuffer[id]

    return testset.samples[img_num]


@app.route('/train/<number>')
def get_train_img(number):
    url = get_dataset_file('train'+'/'+str(number))
    return redirect('/dataset/train/'+url)


@app.route('/test/<number>')
def get_test_img(number):
    url = get_dataset_file('test'+'/'+str(number))
    return redirect('/dataset/test/'+url)


@app.route('/influence-img/<number>')
def get_random_influence_img(number):
    import random
    import math
    random_num = random.randint(1, 1000)
    random_num = math.floor(float(number)*1000)
    url = get_dataset_file('train'+'/'+str(random_num))
    return redirect('/dataset/train/'+url)

# 将编号转化为图片路径


@app.route('/dataset-info/<path:dataOriginId>')
def get_dataset_file(dataOriginId):

    if(datasetFileBuffer.get(dataOriginId)):
        return datasetFileBuffer[dataOriginId]

    dataId = dataOriginId.split("/")
    if dataId[0] == "train":
        if(len(trainset.samples) <= int(dataId[1])):
            return "none"
        filePath = trainset.samples[int(dataId[1])][0]
        filePath = filePath.replace("\\", "/").split("/")
        datasetFileBuffer[dataOriginId] = filePath[-2]+"/"+filePath[-1]
        return get_dataset_file(dataOriginId)
    if dataId[0] == "test":
        if(len(testset.samples) <= int(dataId[1])):
            return "none"
        filePath = testset.samples[int(dataId[1])][0]
        filePath = filePath.replace("\\", "/").split("/")
        datasetFileBuffer[dataOriginId] = filePath[-2]+"/"+filePath[-1]
        return get_dataset_file(dataOriginId)
    if dataId[0] == "test_correct":
        filePath = get_correct(True, int(dataId[1]))[0]
        filePath = filePath.replace("\\", "/").split("/")
        datasetFileBuffer[dataOriginId] = filePath[-2]+"/"+filePath[-1]
        return get_dataset_file(dataOriginId)
    if dataId[0] == "test_mistake":
        filePath = get_correct(False, int(dataId[1]))[0]
        filePath = filePath.replace("\\", "/").split("/")
        datasetFileBuffer[dataOriginId] = filePath[-2]+"/"+filePath[-1]
        return get_dataset_file(dataOriginId)
    return "none"

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
        path = os.path.join(datasetPath, 'type', path)
        print(path)
        result[i] = getPredict(app.model.net, path, 224)
        i += 1
        print("current calculate", i)
    with open('model/model_output'+type+'.json', 'w') as f:
        json.dump(result, f)
    return jsonify(result)


# 将预测结果转换为字符串
def convert_predict_to_string(output):
    result = str(float(output[0]))
    for i in range(1, len(output)):
        result += "_"+str(float(output[i]))
    return result


@app.route('/predictid/<folder>/<imageid>')
def get_predict_img_from_id(folder, imageid):
    url = get_dataset_file(folder+'/'+str(imageid))
    filePath = folder+'/'+url
    return get_predict_img(filePath)


@app.route('/getinfluence/<img_id>/<helpful_num>/<harmful_num>', methods=['POST', 'GET'])
def get_influence_dic(img_id, helpful_num, harmful_num):
    result = {}
    result['success'] = 1
    if(not check_influence(img_id)):
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


if __name__ == "__main__":
    """
    from ml import DataSet, Model, ImageIdConvertor
    #from visual import visualObj
    configs = {'model': 'resnet-18', 'weight': './model/weight/resnet18_cifar_model.pth', 'trainset': './dataset/cifar/train', 'testset': './dataset/cifar/test',
               'classes': './model/cifar-class.txt', 'port': '8000', 'pgd': 'no PGD', 'learn_rate': '0.1', 'epoch': '10', 'shuffle': 'yes', 'device': 'cpu', 'thread': '8', 'batch_size': '128'}
    dataset = DataSet(data_folder='./dataset/ten/',
                      image_size=32, classes_path=configs['classes'])
    model = Model(configs['model'], configs['weight'],
                  configs['device'], pretrained='no')
    load_influence()
    # 这样可以测试
    # print(visualObj.visualize(model.net,'./dataset/cifar/test/0/0_3.jpg',32))
    app.dataset = dataset
    app.model = model
    app.configs = configs
    """
    app.run(port=8000, host="0.0.0.0", debug=True)
