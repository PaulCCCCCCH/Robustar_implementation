import json
import string
import uuid
from flask import request
from flask import Blueprint
from utils.model_utils import *
from objects.RResponse import RResponse
from objects.RServer import RServer

model_api = Blueprint("model_api", __name__)


@model_api.route("/model/current", methods=["GET"])
def GetCurrModel():
    """Get the model that is currently active"""
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
    """return 200 on success"""
    pass


@model_api.route("/model/<id>", methods=["DELETE"])
def DeleteModel():
    """return data
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
    Upload a new model to the server
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

    definitions:
      Metadata:
        type: "object"
        properties:
          class_name:
            type: "string"
            description: "The name of the model class."
            required: true
          nickname:
            type: "string"
            description: "A nickname for the model."
            required: true
          predefined:
            type: "string"
            description: |
                Indicates if a predefined model is being used.
                "1" represents predefined, "0" otherwise.
          description:
            type: "string"
            description: "A description of the model (optional)."
          tags:
            type: "array"
            items:
              type: "string"
            description: "A list of tags associated with the model (optional)."
          pretrained:
            type: "string"
            description: |
              Indicates if a predefined model uses pretrained weights.
              "1" represents pretrained, "0" otherwise (required if predefined).
          num_classes:
            type: "integer"
            description: "The number of classes for the predefined model (required if predefined)."

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
    code_path = None
    weight_path = None
    try:
        # Get the model's metadata
        metadata = json.loads(request.form.get("metadata"))

        try:
            create_models_dir()
        except Exception as e:
            return RResponse.abort(500, f"Failed to create the models directory. {e}")

        print("Requested to upload a new model")

        # Generate a uuid for the model saving
        saving_id = str(uuid.uuid4())

        code_path = os.path.join(
            RServer.get_data_manager().get_base_dir(),
            "generated",
            "models",
            "code",
            f"{saving_id}.py",
        )
        weight_path = os.path.join(
            RServer.get_data_manager().get_base_dir(),
            "generated",
            "models",
            "ckpt",
            f"{saving_id}.pth",
        )

        # Get the model's class name
        class_name = metadata.get("class_name")

        predefined = bool(int(metadata.get("predefined")))

        # Save the model's code definition and initialize the model
        if not predefined:  # If the model is custom
            # Get the model definition code and save it to a temporary file
            code = request.form.get("code")
            if code is None:
                return RResponse.fail(f"The model definition code is missing.", 400)
            try:
                save_code(code, code_path)
            except Exception as e:
                clear_model_temp_files(code_path, weight_path)
                return RResponse.abort(500, f"Failed to save the model definition. {e}")
            # Initialize the model
            try:
                model = init_custom_model(code_path, class_name)
            except Exception as e:
                clear_model_temp_files(code_path, weight_path)
                return RResponse.fail(
                    f"Failed to initialize the custom model. {e}", 400
                )
        elif predefined:  # If the model is predefined
            pretrained = bool(int(metadata.get("pretrained")))
            num_classes = int(metadata.get("num_classes"))
            code = f"num_classes = {num_classes}"
            try:
                save_code(code, code_path)
            except Exception as e:
                clear_model_temp_files(code_path, weight_path)
                return RResponse.abort(500, f"Failed to save the model definition. {e}")
            try:
                model = init_predefined_model(class_name, pretrained, num_classes)
            except Exception as e:
                clear_model_temp_files(code_path, weight_path)
                return RResponse.fail(
                    f"Failed to initialize the predefined model. {e}", 400
                )
        else:
            return RResponse.fail(
                "Invalid request. The model is neither custom nor predefined.", 400
            )

        # Get the weight file and save it to a temporary location if it exists
        if "weight_file" in request.files:
            weight_file = request.files.get("weight_file")
            try:
                save_ckpt_weight(weight_file, weight_path)
            except Exception as e:
                clear_model_temp_files(code_path, weight_path)
                return RResponse.abort(500, f"Failed to save the weight file. {e}")
            # Load and validate the weights from the file
            try:
                load_ckpt_weight(model, weight_path)
            except Exception as e:
                clear_model_temp_files(code_path, weight_path)
                return RResponse.fail(f"Failed to load the weights. {e}", 400)
        else:  # If the weight file is not provided, save the current weights to a temporary location
            try:
                save_cur_weight(model, weight_path)
            except Exception as e:
                clear_model_temp_files(code_path, weight_path)
                return RResponse.abort(500, f"Failed to save the weight file. {e}")

        # Validate the model
        try:
            val_model(model)
        except Exception as e:
            clear_model_temp_files(code_path, weight_path)
            return RResponse.fail(f"The model is invalid. {e}", 400)

        # Construct the metadata for saving
        try:
            metadata_4_save = construct_metadata_4_save(
                class_name, metadata, code_path, weight_path, model
            )
        except Exception as e:
            clear_model_temp_files(code_path, weight_path)
            return RResponse.abort(
                500, f"Failed to construct the metadata for saving. {e}"
            )

        # Save the model's metadata to the database
        try:
            RServer.get_model_manager().create_model(metadata_4_save)
        except Exception as e:
            clear_model_temp_files(code_path, weight_path)
            return RResponse.abort(
                500, f"Failed to save the model to the database. {e}"
            )

        # Set the current model to the newly uploaded model
        try:
            SetCurrModel(saving_id)
        except Exception as e:
            clear_model_temp_files(code_path, weight_path)
            return RResponse.abort(500, f"Failed to set the current model. {e}")

        return RResponse.ok("Success")
    except Exception as e:
        if code_path is not None and weight_path is not None:
            clear_model_temp_files(code_path, weight_path)
        return RResponse.abort(500, f"Unexpected error. {e}")


@model_api.route("/model/list", methods=["GET"])
def GetAllModels():
    """return data
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
