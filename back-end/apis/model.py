import string
import os
import torch
from flask import request
from flask import Blueprint
from utils.model_utils import init_model_from_def, val_model, save_model
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
    After training a model, should do the same
    ---
    tags:
      - model
    consumes:
      - "multipart/form-data"
    produces:
      - "application/json"
    parameters:
      - in: "formData"        # Use "formData" to indicate multipart/form-data parameters
        name: "model_def"     # Name of the parameter for the model definition code
        description: "The definition of the model in Python code"
        required: true
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
    print("Requested to upload a model")

    # Get the model definition code and save it to a temporary file
    model_def = request.form.get('model_def')
    # TODO: discuss with team the path to save the temp file
    def_file_path = os.path.join(RServer.get_server().base_dir, 'temp_def.py')
    try:
        with open(def_file_path, 'w') as temp_file:
            temp_file.write(model_def)
    except Exception as e:
        # Delete the temporary definition file and return
        os.remove(def_file_path)
        return RResponse.abort(500, f"Failed to save the model definition. {e}")

    # Initialize the model
    try:
        model = init_model_from_def(def_file_path)
    except Exception as e:
        # Delete the temporary definition file and return
        os.remove(def_file_path)
        return RResponse.abort(400, f"Failed to initialize the model. {e}")

    # Get the weight file and save it to a temporary location if it exists
    weight_file = request.files.get('weight_file')
    if weight_file is not None:
        try:
            weight_file_path = os.path.join(RServer.get_server().base_dir, 'temp_weights.pth')
            weight_file.save(weight_file_path)
        except Exception as e:
            # Delete the weight file
            os.remove(weight_file_path)
            return RResponse.abort(500, f"Failed to save the weight file. {e}")

    # Load the weights from the file
    try:
        model.load_state_dict(torch.load(weight_file_path))
    except Exception as e:
        # Delete the temp files
        os.remove(def_file_path)
        os.remove(weight_file_path)
        return RResponse.abort(400, f"Failed to load the weight. {e}")

    # Validate the model
    try:
        val_model(model)
    except Exception as e:
        # Delete the temp files
        os.remove(def_file_path)
        os.remove(weight_file_path)
        return RResponse.abort(400, f"The model is invalid. {e}")

    # TODO: generate a real model id
    model_id = "abc123"

    # Save the model to the database
    try:
        save_model(model)
    except Exception as e:
        # Delete the temp files
        os.remove(def_file_path)
        os.remove(weight_file_path)
        return RResponse.abort(500, f"Failed to save the model. {e}")

    # Set the current model to the newly uploaded model
    try:
        SetCurrModel(model_id)
    except Exception as e:
        # Delete the temp files
        os.remove(def_file_path)
        os.remove(weight_file_path)
        return RResponse.abort(500, f"Failed to set the current model. {e}")

    # TODO: return real data as specified in the docstring
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

