import json
import os.path as osp
import os
from objects.RServer import RServer
from objects.RDataManager import RDataManager
from objects.RAutoAnnotator import RAutoAnnotator
from utils.train import initialize_model
from utils.path_utils import to_unix, to_absolute
from flask import Flask
import argparse
from flask_socketio import emit, SocketIO
from apis import blueprints


def start_flask_app():
    def afterRequest(resp):
        resp.headers["Access-Control-Allow-Origin"] = "*"
        resp.headers["Access-Control-Allow-Headers"] = "*"
        return resp

    app = Flask(__name__)
    app.after_request(afterRequest)

    # register all api routes
    for bp in blueprints:
        # TODO: use /api/<version> prefix
        # app.register_blueprint(bp, url_prefix='/api/v1')
        app.register_blueprint(bp)

    socket = SocketIO(app, cors_allowed_origins="*")

    return app, socket


# Get server listener objects
app, socket = start_flask_app()

# Init socket connection
@socket.on("connect")
def test_connect():
    print("Successfully connected to frontend with socket")
    emit("afterConnect", {"data": "Lets dance"})


def precheck():
    def check_num_classes_consistency():
        configs = RServer.getServerConfigs()
        data_manager = RServer.getDataManager()
        trainset = data_manager.trainset
        testset = data_manager.testset
        validationset = data_manager.validationset

        classes_num = configs["num_classes"]
        error_template = "Number of classes specified in configs.json({}) doesn't match that in dataset {}({})"
        errors = []
        if len(trainset.classes) != classes_num:
            errors.append(
                error_template.format(
                    classes_num, "Training Set", len(trainset.classes)
                )
            )
        if len(testset.classes) != classes_num:
            errors.append(
                error_template.format(classes_num, "Test Set", len(trainset.classes))
            )
        if len(validationset.classes) != classes_num:
            errors.append(
                error_template.format(
                    classes_num, "Validation Set", len(trainset.classes)
                )
            )
        assert len(errors) == 0, "\n".join(errors)

    check_num_classes_consistency()


def new_server_object(basedir):
    baseDir = to_unix(basedir)
    datasetDir = to_unix(osp.join(baseDir, "dataset"))
    ckptDir = to_unix(osp.join(baseDir, "checkpoints"))
    dbPath = to_unix(osp.join(baseDir, "data.db"))

    with open(osp.join(baseDir, "configs.json")) as jsonfile:
        configs = json.load(jsonfile)

    class2labelPath = osp.join(baseDir, "class2label.json")
    class2labelMapping = {}
    if osp.exists(class2labelPath):
        try:
            with open(class2labelPath) as jsonfile:
                class2labelMapping = json.load(jsonfile)
                print("Class to label file loaded!")
        except Exception as e:
            print("Class to label file invalid!")
            class2labelMapping = {}
    else:
        print("Class to label file not found!")

    # Create server

    # Set data manager
    server = RServer.createServer(
        configs=configs,
        baseDir=baseDir,
        datasetDir=datasetDir,
        ckptDir=ckptDir,
        app=app,
        socket=socket,
    )
    dataManager = RDataManager(
        baseDir,
        datasetDir,
        dbPath,
        batch_size=configs["batch_size"],
        shuffle=configs["shuffle"],
        num_workers=configs["num_workers"],
        image_size=configs["image_size"],
        image_padding=configs["image_padding"],
        class2label_mapping=class2labelMapping,
    )
    RServer.setDataManager(dataManager)

    # Set model (used for prediction)
    model = initialize_model()
    RServer.setModel(model)

    # Set auto annotator
    # TODO: model_name and checkpoint hard-coded for now
    checkpoint_name = "u2net.pth"
    annotator = RAutoAnnotator(
        configs["device"],
        checkpoint=osp.join(baseDir, checkpoint_name),
        model_name="u2net",
    )
    RServer.setAutoAnnotator(annotator)

    # Check file state consistency
    precheck()


def get_args():
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--basedir",
        default="/Robustar2",
        help="path to base directory for data folder (default: /Robustar2)",
    )

    args = parser.parse_known_args()[0]
    return args


def create_app():
    args = get_args()

    # Get basedir
    basedir = to_absolute(os.getcwd(), to_unix(args.basedir))
    print("Current working directory is {}".format(os.getcwd()))
    print("Absolute basedir is {}".format(basedir))
    new_server_object(basedir)

    return RServer.getServer().getFlaskApp()


if __name__ == "__main__":
    # Start server
    create_app().run(port="8000", host="0.0.0.0", debug=False)
