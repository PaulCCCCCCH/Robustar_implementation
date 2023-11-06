from .RDataManager import RDataManager
from .RModelWrapper import RModelWrapper
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
        self.model_weights = {}

    @staticmethod
    def create_server(
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
    def get_server():
        return RServer.server_instance

    @staticmethod
    def get_data_manager() -> RDataManager:
        return RServer.server_instance.data_manager

    @staticmethod
    def set_data_manager(data_manager):
        RServer.server_instance.data_manager = data_manager

    @staticmethod
    def get_auto_annotator():
        return RServer.server_instance.auto_annotator

    @staticmethod
    def set_auto_annotator(auto_annotator):
        RServer.server_instance.auto_annotator = auto_annotator

    @staticmethod
    def get_server_configs():
        return RServer.server_instance.configs

    @staticmethod
    def get_model_wrapper() -> RModelWrapper:
        return RServer.server_instance.model_wrapper

    @staticmethod
    def set_model(model_wrapper):
        RServer.server_instance.model_wrapper = model_wrapper

    @staticmethod
    def get_model_weights():
        return RServer.server_instance.model_weights

    @staticmethod
    def add_model_weight(name, weight):
        RServer.server_instance.model_weights[name] = weight

    @staticmethod
    def get_socket():
        return RServer.get_server().socket

    def get_flask_app(self):
        return self.app

    def run(self, port=8000, host="0.0.0.0", debug=True):
        self.port = port
        self.host = host
        self.debug = debug
        # self.app.run(port=port, host=host, debug=debug)
        self.socket.run(self.app, port=port, host=host, debug=debug)
