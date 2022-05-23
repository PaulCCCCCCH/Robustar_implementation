from .RDataManager import RDataManager
from flask import Flask, Blueprint
from flasgger import Swagger
import os.path as osp
from flask_socketio import SocketIO


# Wrapper for flask server instance
class RServer:

    serverInstance = None

    # Use createServer method instead!
    def __init__(self, configs, baseDir, datasetDir, ckptDir):
    
        app = Flask(__name__)
        app.after_request(self.afterRequest)
        socket_ = SocketIO(app, cors_allowed_origins='*')
        self.socket_ = socket_

        # TODO: use /api/<version> prefix
        # self.bp = Blueprint('api', __name__, url_prefix='/api/v1')
        self.bp = Blueprint('api', __name__)
        
        app.config['SWAGGER'] = {
            'title': 'Robustar API',
            'uiversion': 3,
            'version': 'beta'
        }
        swagger = Swagger(app)

        self.datasetDir = datasetDir
        self.baseDir = baseDir
        self.datasetPath = datasetDir
        self.ckptDir = ckptDir
        self.app = app
        self.configs = configs
        self.modelWrapper = None
        self.modelsWeights = {}

    @staticmethod
    def createServer(configs: dict, baseDir: str, datasetDir: str, ckptDir: str):
        if RServer.serverInstance is None:
            RServer.serverInstance = RServer(configs, baseDir, datasetDir, ckptDir)
        else:
            assert configs == RServer.serverInstance.configs, \
            'Attempting to recreate an existing server with different configs'
        return RServer.serverInstance

   
    
    @staticmethod
    def getServer():
        return RServer.serverInstance

    @staticmethod
    def getDataManager() -> RDataManager:
        return RServer.serverInstance.dataManager

    @staticmethod
    def setDataManager(dataManager):
        RServer.serverInstance.dataManager = dataManager

    @staticmethod
    def getAutoAnnotator():
        return RServer.serverInstance.autoAnnotator

    @staticmethod
    def setAutoAnnotator(autoAnnotator):
        RServer.serverInstance.autoAnnotator = autoAnnotator

    @staticmethod
    def getServerConfigs():
        return RServer.serverInstance.configs

    @staticmethod
    def getModelWrapper():
        return RServer.serverInstance.modelWrapper

    @staticmethod
    def setModel(modelWrapper):
        RServer.serverInstance.modelWrapper = modelWrapper

    @staticmethod
    def getModelsWeights():
        return RServer.serverInstance.modelsWeights

    @staticmethod
    def addModelWeight(name, weight):
        RServer.serverInstance.modelsWeights[name] = weight

    @staticmethod
    def getSocket():
        return RServer.getServer().socket_

    @staticmethod
    def registerAPIs():
        import apis
        server = RServer.getServer()
        server.getFlaskApp().register_blueprint(server.bp)
    
    def afterRequest(self, resp):
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = '*'
        return resp

    def getFlaskApp(self):
        return self.app

    def getFlaskBluePrint(self):
        return self.bp

    def run(self, port=8000, host='0.0.0.0', debug=True):
        self.port = port
        self.host = host
        self.debug = debug
        # self.app.run(port=port, host=host, debug=debug)
        self.socket_.run(self.app, port=port, host=host, debug=debug)