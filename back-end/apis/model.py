import traceback
from flask import request
from flask import Blueprint
from utils.model_utils import *
from objects.RResponse import RResponse
from objects.RServer import RServer
from objects.RModelWrapper import RModelWrapper

model_api = Blueprint("model_api", __name__)


@model_api.route("/model/current", methods=["GET"])
def get_curr_model():
    model = RServer.get_model_wrapper().get_current_model_metadata()
    if not model:
        RResponse.abort(400, f"No current model is selected")

    return RResponse.ok(model.as_dict())


@model_api.route("/model/current/<int:model_id>", methods=["POST"])
def set_curr_model(model_id: int):
    """return 200 on success"""
    try:
        RServer.get_model_wrapper().set_current_model(model_id)
        return RResponse.ok("Success")
    except Exception as e:
        traceback.print_exc()
        RResponse.abort(500, f"Failed to switch to model {model_id}. Error: {str(e)}")


@model_api.route("/model/<int:model_id>", methods=["DELETE"])
def delete_model(model_id: int):
    """
    return model meta data
    """
    try:
        model = RServer.get_model_wrapper().delete_model_by_id(model_id)
    except ValueError as e:
        RResponse.abort(400, f"Failed to delete model {model_id}. Error: {str(e)}")
    except Exception as e:
        traceback.print_exc()
        RResponse.abort(500, f"Failed to delete model {model_id}. Error: {str(e)}")

    if not model:
        RResponse.abort(400, f"Model {model_id} does not exist.")

    return RResponse.ok(model.as_dict())


@model_api.route("/model", methods=["POST"])
def upload_model():
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
            required: true
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
              Indicates whether the model is pretrained.
              Should only be set to "1" if the model is predefined and pretrained.

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
    cm = ContextManager()
    with cm:
        # Precheck the request
        try:
            precheck_request_4_upload_model(request)
        except Exception as e:
            RResponse.abort(400, f"Request validation failed. Error: {e}")

        metadata_str = request.form.get("metadata")
        metadata = json.loads(metadata_str)

        print("Requested to upload a new model")

        # Get the model's class name
        class_name = metadata.get("class_name")

        predefined = bool(int(metadata.get("predefined")))

        # Save the model's code definition and initialize the model
        if not predefined:  # If the model is custom
            cm.init_code_path()

            # Get the model definition code and save it to a temporary file
            code = request.form.get("code")
            save_code(code, cm.code_path)
            # Initialize the model
            try:
                model = RServer.get_model_wrapper().init_custom_model(
                    cm.code_path, class_name
                )
            except Exception as e:
                RResponse.abort(400, f"Failed to initialize the custom model. {str(e)}")
        elif predefined:  # If the model is predefined
            pretrained = bool(int(metadata.get("pretrained")))
            try:
                model = RServer.get_model_wrapper().init_predefined_model(
                    class_name, pretrained
                )
            except Exception as e:
                RResponse.abort(
                    400, f"Failed to initialize the predefined model. Error: {str(e)}"
                )

        # Get the weight file and save it to a temporary location if it exists
        if "weight_file" in request.files:
            cm.init_weight_path()
            weight_file = request.files.get("weight_file")
            save_ckpt_weight(weight_file, cm.weight_path)
            # Load and validate the weights from the file
            try:
                load_ckpt_weight(model, cm.weight_path)
            except Exception as e:
                RResponse.abort(400, f"Failed to load the weights. Error: {str(e)}")

        # Validate the model
        try:
            dummy_model_wrapper = DummyModelWrapper(
                model, RServer.get_model_wrapper().device
            )
            val_model(dummy_model_wrapper)
        except Exception as e:
            RResponse.abort(400, f"The model is invalid. {e}")

        # Construct the metadata for saving
        metadata_4_save = construct_metadata_4_save(
            metadata, cm.code_path, cm.weight_path, model
        )

        # Save the model's metadata to the database
        try:
            model = RServer.get_model_wrapper().create_model(metadata_4_save)

            ## Set the current model to the newly uploaded model
            ## TODO(Chonghan): Removing this logic for better separation of concern during tests.
            ## We may want to add this back in the future.
            # RServer.get_model_wrapper().set_current_model(metadata.get("nickname"))
            return RResponse.ok(model.as_dict())
        except Exception as e:
            RResponse.abort(400, f"Failed to save the model. Error: {str(e)}")




@model_api.route("/model/<int:model_id>", methods=["PUT"])
def update_model(model_id: int):
    """
    path_parameter:
        model_name: nickname of the model
    request_body:
        metadata: see upload_model API definition
    returns:
        model meta data
    """
    try:
        metadata_str = request.form.get("metadata")
        metadata = json.loads(metadata_str)
        model = RServer.get_model_wrapper().update_model(model_id, metadata)
        if not model:
            return RResponse.abort(
                400, f"Failed to update model.Model {model_id} not found."
            )
        return RResponse.ok(model.as_dict())
    except Exception as e:
        traceback.print_exc()
        return RResponse.abort(500, f"Failed to update model. Error: {str(e)}")


@model_api.route("/model/duplicate/<int:model_id>", methods=["POST"])
def duplicate_model(model_id: int):
    """
    return model metadata for the duplicated model
    """
    try:
        model = RServer.get_model_wrapper().duplicate_model(model_id)
        if not model:
            return RResponse.abort(
                400, f"Failed to duplicate model. Model {model_id} not found."
            )
        return RResponse.ok(model.as_dict())
    except Exception as e:
        traceback.print_exc()
        return RResponse.abort(500, f"Failed to duplicate model. Error: {str(e)}")


@model_api.route("/model/list", methods=["GET"])
def get_all_models():
    """
    return a list of model metadata
    """
    try:
        return RResponse.ok(
            [model.as_dict() for model in RServer.get_model_wrapper().list_models()]
        )
    except Exception as e:
        traceback.print_exc()
        return RResponse.abort(500, f"Failed to list all models. {str(e)}")


@model_api.route("/model/predefined", methods=["GET"])
def get_predefined_models():
    """
    return a list of pre-defined model names
    """
    return RResponse.ok(RModelWrapper.list_predefined_models())
