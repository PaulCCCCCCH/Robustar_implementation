import json
import string
import uuid
import io
import contextlib
from flask import request
from flask import Blueprint
from datetime import datetime
from utils.model_utils import *
from objects.RResponse import RResponse
from objects.RServer import RServer

model_api = Blueprint("model_api", __name__)

@model_api.route("/model/current", methods=["GET"])
def GetCurrModel():
    """ Get the model that is currently active """
    """ return data
    {
        id: string,
        name: string,
        details: string,
    }
    """
    pass


@model_api.route("/model/current/<model_id>", methods=["POST"])
def SetCurrModel(model_id: string):
    """ return 200 on success """
    pass


@model_api.route("/model/<id>", methods=["DELETE"])
def DeleteModel():
    """ return data
    {
        id: string,
        name: string,
        details: string,
    }
    """
    pass


@model_api.route("/model", methods=["POST"])
def UploadModel():
    """
    Should also accept (optionally) a model weight file as argument
    ---
    tags:
      - model
    consumes:
      - "multipart/form-data"
    produces:
      - "application/json"
    parameters:
      - in: "formData"        # Use "formData" to indicate multipart/form-data parameters
        name: "metadata"      # Name of the parameter for the model metadata
        description: "The metadata of the model"
        required: true        # The metadata is required, so set 'required' to true
        type: "string"        # The type of data for the metadata
      - in: "formData"        # Use "formData" to indicate multipart/form-data parameters
        name: "code"          # Name of the parameter for the model definition code
        description: "The definition of the model in Python code"
        required: false       # The model definition code is optional, so set 'required' to false
        type: "string"        # The type of data for the model definition code
      - in: "formData"        # Use "formData" to indicate multipart/form-data parameters
        name: "weight_file"   # Name of the parameter for the model weight file
        description: "The weight file for the trained model (optional)"
        required: false       # The weight file is optional, so set 'required' to false
        type: "file"          # The type of data for the weight file (file upload)

    responses:
      200:
        description: Model uploaded successfully
        schema:
          type: "object"
          properties:
            code:
              type: "integer"
              example: 0
            data:
              type: "object"
              properties:
                id:
                  type: "string"
                  example: "abc123"
                name:
                  type: "string"
                  example: "NewModel"
                details:
                  type: "string"
                  example: "Uploaded successfully"
            msg:
              type: "string"
              example: "Success"

    """
    # Get the model's metadata
    metadata = json.loads(request.form.get('metadata'))

    # Check if the folder for saving models exists, if not, create it
    models_dir = os.path.join(RServer.get_server().base_dir, 'generated', 'models')
    if not os.path.exists(models_dir):
        os.makedirs(models_dir)

    print("Requested to upload a new model")

    # Generate a uuid for the model saving
    saving_id = str(uuid.uuid4())

    code_path = os.path.join(RServer.get_server().base_dir, 'generated', 'models', f'{saving_id}.py')

    metadata_4_save = {'class_name': None,
                       'nickname': None,
                       'description': None,
                       'architecture': None,
                       'tags': None,
                       'create_time': None,
                       'weight_path': None,
                       'code_path': None,
                       'epoch': None,
                       'train_accuracy': None,
                       'val_accuracy': None,
                       'test_accuracy': None,
                       'last_eval_on_dev_set': None,
                       'last_eval_on_test_set': None
                       }

    # Get the model's class name
    class_name = metadata.get('class_name')

    # If the model is custom(i.e. it has code definition)
    if 'code' in request.form:
        # Get the model definition code and save it to a temporary file
        code = request.form.get('code')
        try:
            with open(code_path, 'w') as code_file:
                code_file.write(code)
        except Exception as e:
            clear_model_temp_files(saving_id)
            return RResponse.abort(500, f"Failed to save the model definition. {e}")

        # Initialize the custom model
        try:
            model = init_custom_model(code_path, class_name)
        except Exception as e:
            clear_model_temp_files(saving_id)
            return RResponse.abort(400, f"Failed to initialize the custom model. {e}")
    else:   # If the model is predefined
        pretrained = bool(int(metadata.get('pretrained')))
        num_classes = int(metadata.get('num_classes'))
        try:
            model = init_predefined_model(class_name, pretrained, num_classes)
            with open(code_path, 'w') as code_file:
                code_file.write(f"num_classes = {num_classes}")
        except Exception as e:
            return RResponse.abort(400, f"Failed to initialize the predefined model. {e}")

    # Get the weight file and save it to a temporary location if it exists
    if 'weight_file' in request.files:
        weight_file = request.files.get('weight_file')
        try:
            weight_path = os.path.join(RServer.get_server().base_dir, 'generated', 'models', f'{saving_id}.pth')
            weight_file.save(weight_path)
        except Exception as e:
            clear_model_temp_files(saving_id)
            return RResponse.abort(500, f"Failed to save the weight file. {e}")

        # Load the weights from the file
        try:
            model.load_state_dict(torch.load(weight_path))
        except Exception as e:
            clear_model_temp_files(saving_id)
            return RResponse.abort(400, f"Failed to load the weights. {e}")
    else:   # If the weight file is not provided, save the current weights to a temporary location
        try:
            weight_path = os.path.join(RServer.get_server().base_dir, 'generated', 'models', f'{saving_id}.pth')
            torch.save(model.state_dict(), weight_path)
        except Exception as e:
            clear_model_temp_files(saving_id)
            return RResponse.abort(500, f"Failed to save the weight file. {e}")

    # Validate the model
    try:
        val_model(model)
    except Exception as e:
        clear_model_temp_files(saving_id)
        return RResponse.abort(400, f"The model is invalid. {e}")

    # Update the metadata for saving
    metadata_4_save['class_name'] = class_name
    metadata_4_save['nickname'] = metadata.get('nickname')
    metadata_4_save['description'] = metadata.get('description') if metadata.get('description') else None
    metadata_4_save['tags'] = metadata.get('tags') if metadata.get('tags') else None
    metadata_4_save['create_time'] = datetime.now()
    metadata_4_save['code_path'] = code_path
    metadata_4_save['weight_path'] = weight_path
    metadata_4_save['epoch'] = 0
    metadata_4_save['train_accuracy'] = None
    metadata_4_save['val_accuracy'] = None
    metadata_4_save['test_accuracy'] = None
    metadata_4_save['last_eval_on_dev_set'] = None
    metadata_4_save['last_eval_on_test_set'] = None

    # Save the model's architecture to the metadata
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        print(model)
    metadata_4_save['architecture'] = buffer.getvalue()

    # Save the model's metadata to the database
    try:
        RServer.get_model_wrapper().create_model(metadata_4_save)
    except Exception as e:
        return RResponse.abort(500, f"Failed to save the model. {e}")

    # Set the current model to the newly uploaded model
    try:
        SetCurrModel(saving_id)
    except Exception as e:
        return RResponse.abort(500, f"Failed to set the current model. {e}")

    return RResponse.ok('Success')


@model_api.route("/model/list", methods=["GET"])
def GetAllModels():
    """ return data
    [
        {
            id: string,
            name: string,
            details: string,
        },
        ...
    ]
    """
    pass

