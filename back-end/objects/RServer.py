'''
Author: Chonghan Chen (paulcccccch@gmail.com)
-----
Last Modified: Thursday, 18th November 2021 12:18:49 am
Modified By: Chonghan Chen (paulcccccch@gmail.com)
-----
'''

from .RDataManager import RDataManager
from flask import Flask
import os.path as osp


# Wrapper for flask server instance
class RServer:

    serverInstance = None

    # Use createServer method instead!
    def __init__(self, configs, baseDir, datasetDir):
    
        app = Flask(__name__)
        app.after_request(self.afterRequest)

        self.datasetDir = datasetDir
        self.baseDir = baseDir
        self.datasetPath = datasetDir
        self.app = app
        self.configs = configs
        self.modelWrapper = None

    @staticmethod
    def createServer(configs: dict, baseDir: str, datasetDir: str):
        if RServer.serverInstance is None:
            RServer.serverInstance = RServer(configs, baseDir, datasetDir)
        else:
            assert configs == RServer.serverInstance.configs, \
            'Attempting to recreate an existing server with different configs'
        return RServer.serverInstance

   
    
    @staticmethod
    def getServer():
        return RServer.serverInstance

    @staticmethod
    def getDataManager():
        return RServer.serverInstance.dataManager

    @staticmethod
    def setDataManager(dataManager):
        RServer.serverInstance.dataManager = dataManager

    @staticmethod
    def getServerConfigs():
        return RServer.serverInstance.configs

    @staticmethod
    def getModelWrapper():
        return RServer.serverInstance.modelWrapper

    @staticmethod
    def setModel(modelWrapper):
        RServer.serverInstance.modelWrapper = modelWrapper
        
    
    def afterRequest(self, resp):
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = '*'
        return resp

    def getFlaskApp(self):
        return self.app

    def run(self, port=8000, host='0.0.0.0', debug=True):
        self.port = port
        self.host = host
        self.debug = debug
        self.app.run(port=port, host=host, debug=debug)