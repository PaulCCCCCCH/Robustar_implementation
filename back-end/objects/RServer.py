from .RDataManager import RDataManager
from flasgger import Swagger


# Wrapper for flask server instance
class RServer:

    server_instance = None

    # Use createServer method instead!
    def __init__(self, configs, base_dir, dataset_dir, ckpt_dir, app, socket):

        app.config["SWAGGER"] = {
            "title": "Robustar API",
            "uiversion": 3,
            "version": "beta",
        }
        self.swagger = Swagger(app)

        self.dataset_dir = dataset_dir
        self.base_dir = base_dir
        self.datasetPath = dataset_dir
        self.ckpt_dir = ckpt_dir
        self.app = app
        self.socket = socket
        self.configs = configs
        self.model_wrapper = None
        self.modelsWeights = {}

    @staticmethod
    def createServer(
        configs: dict, base_dir: str, dataset_dir: str, ckpt_dir: str, app, socket
    ):
        if RServer.server_instance is None:
            RServer.server_instance = RServer(
                configs, base_dir, dataset_dir, ckpt_dir, app, socket
            )
        else:
            assert (
                configs == RServer.server_instance.configs
            ), "Attempting to recreate an existing server with different configs"
        return RServer.server_instance

    @staticmethod
    def getServer():
        return RServer.server_instance

    @staticmethod
    def getDataManager() -> RDataManager:
        return RServer.server_instance.dataManager

    @staticmethod
    def setDataManager(dataManager):
        RServer.server_instance.dataManager = dataManager

    @staticmethod
    def getAutoAnnotator():
        return RServer.server_instance.autoAnnotator

    @staticmethod
    def setAutoAnnotator(autoAnnotator):
        RServer.server_instance.autoAnnotator = autoAnnotator

    @staticmethod
    def getServerConfigs():
        return RServer.server_instance.configs

    @staticmethod
    def getModelWrapper():
        return RServer.server_instance.model_wrapper

    @staticmethod
    def setModel(model_wrapper):
        RServer.server_instance.model_wrapper = model_wrapper

    @staticmethod
    def getModelsWeights():
        return RServer.server_instance.modelsWeights

    @staticmethod
    def addModelWeight(name, weight):
        RServer.server_instance.modelsWeights[name] = weight

    @staticmethod
    def getSocket():
        return RServer.getServer().socket

    def getFlaskApp(self):
        return self.app

    def run(self, port=8000, host="0.0.0.0", debug=True):
        self.port = port
        self.host = host
        self.debug = debug
        # self.app.run(port=port, host=host, debug=debug)
        self.socket.run(self.app, port=port, host=host, debug=debug)
