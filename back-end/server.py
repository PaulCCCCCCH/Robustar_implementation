import torchvision.datasets as dset
import json
import os
import os.path as osp
from flask import Flask, render_template, redirect, send_from_directory, request, jsonify, Response
from objects.RServer import RServer
from objects.RDataManager import RDataManager
from utils.train import initialize_model

from influence import check_influence, load_influence, get_helpful_list, get_harmful_list, get_influence_list


# TODO: The following are for reference only
def register_route(app):
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
            if exist: reply = QMessageBox.question(
                    self, 'Message', 'Another model is already saved here and it may be over written. Are you sure?',
                    QMessageBox.Yes , QMessageBox.No
                )
                if reply == QMessageBox.Yes:
                    exist = False
            if not exist:
                self.saveToEdit.setText(saveFolder)
            """
        pass

    @app.route('/main/<path:path>')
    def main_route(path):
        return send_from_directory("web", path)

    @app.route('/img/<filename>')
    def get_file_page(filename):
        return send_from_directory("./img", filename)

    @app.route('/data/chart-labels.js')
    def get_chart_labels():
        return "window.labels='23333'"

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
        return send_from_directory("./visualize", 'img-' + str(num) + '.png')

    datasetFileBuffer = {}
    predictBuffer = {}

    # 用来记录正确的分类结果和错误的分类结果
    correctTestBuffer, incorrectTestBuffer, correctValidationBuffer, incorrectValidationBuffer = None, None, None, None


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
    baseDir = osp.join('/', 'Robustar2').replace('\\', '/')
    datasetDir = osp.join(baseDir, 'dataset').replace('\\', '/')

    with open(osp.join(baseDir, 'configs.json')) as jsonfile:
        configs = json.load(jsonfile)

    server = RServer.createServer(configs=configs, baseDir=baseDir, datasetDir=datasetDir)
    dataManager = RDataManager(
        baseDir, datasetDir, 
        batch_size=configs['batch_size'], 
        shuffle=configs['shuffle'],
        num_workers=configs['num_workers'],
        image_size=configs['image_size'],
        image_padding=configs['image_padding'],
    )
    RServer.setDataManager(dataManager)

    model = initialize_model()
    RServer.setModel(model)
    import apis # register all api routes


    server.run(port='8000', host='0.0.0.0', debug=False)
