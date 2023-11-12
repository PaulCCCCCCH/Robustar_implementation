import uuid
import traceback
from flask import request
from flask import Blueprint
from utils.model_utils import *
from objects.RResponse import RResponse
from objects.RServer import RServer
from objects.RModelWrapper import RModelWrapper

model_api = Blueprint("model_api", __name__)


@model_api.route("/model/current", methods=["GET"])
def GetCurrModel():
    model = RServer.get_model_wrapper().get_current_model_metadata()
    if not model:
        RResponse.abort(400, f"No current model is selected")

    return RResponse.ok(model.as_dict())


@model_api.route("/model/current/<model_name>", methods=["POST"])
def SetCurrModel(model_name: str):
    """return 200 on success"""
    try:
        RServer.get_model_wrapper().set_current_model(model_name)
        return RResponse.ok("Success")
    except Exception as e:
        RResponse.abort(500, "Failed to switch model." + str(e))


@model_api.route("/model/<model_name>", methods=["DELETE"])
def DeleteModel(model_name: str):
    """return data
    {
        id: integer,
        name: string,
        details: string,
    }
    """
    try:
        model = RServer.get_model_wrapper().delete_model_by_name(model_name)
    except Exception as e:
        RResponse.abort(500, f"Failed to delete model {model_name}." + str(e))

    if not model:
        RResponse.abort(400, f"Model {model_name} does not exist.")

    return RResponse.ok(model.as_dict())


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
    code_path = None
    weight_path = None
    try:
        # Precheck the request
        errors = precheck_request_4_upload_model(request)
        if len(errors) > 0:
            error_message = "; ".join(errors)
            return RResponse.fail(f"Request validation failed: {error_message}", 400)

        metadata_str = request.form.get("metadata")
        metadata = json.loads(metadata_str)

        # Create the code and ckpt directories if they don't exist
        create_models_dir()

        print("Requested to upload a new model")

        # Generate a uuid for the model saving
        saving_id = str(uuid.uuid4())

        # Get the model's class name
        class_name = metadata.get("class_name")

        predefined = bool(int(metadata.get("predefined")))

        # Save the model's code definition and initialize the model
        if not predefined:  # If the model is custom
            code_path = os.path.join(
                RServer.get_server().base_dir,
                "generated",
                "models",
                "code",
                f"{saving_id}.py",
            )

            # Get the model definition code and save it to a temporary file
            code = request.form.get("code")
            save_code(code, code_path)
            # Initialize the model
            try:
                model = RModelWrapper.init_custom_model(
                    code_path, class_name, RServer.get_model_wrapper().device
                )
            except Exception as e:
                traceback.print_exc()
                clear_model_temp_files(code_path, weight_path)
                return RResponse.fail(
                    f"Failed to initialize the custom model. {e}", 400
                )
        elif predefined:  # If the model is predefined
            pretrained = bool(int(metadata.get("pretrained")))
            num_classes = RServer.get_data_manager().get_num_classes()
            try:
                model = RModelWrapper.init_predefined_model(
                    class_name,
                    pretrained,
                    num_classes,
                    RServer.get_model_wrapper().device,
                )
            except Exception as e:
                traceback.print_exc()
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
            weight_path = os.path.join(
                RServer.get_server().base_dir,
                "generated",
                "models",
                "ckpt",
                f"{saving_id}.pth",
            )
            weight_file = request.files.get("weight_file")
            save_ckpt_weight(weight_file, weight_path)
            # Load and validate the weights from the file
            try:
                load_ckpt_weight(model, weight_path)
            except Exception as e:
                traceback.print_exc()
                clear_model_temp_files(code_path, weight_path)
                return RResponse.fail(f"Failed to load the weights. {e}", 400)

        # Validate the model
        try:
            dummy_model_wrapper = DummyModelWrapper(
                model, RServer.get_model_wrapper().device
            )
            val_model(dummy_model_wrapper)
        except Exception as e:
            traceback.print_exc()
            clear_model_temp_files(code_path, weight_path)
            return RResponse.fail(f"The model is invalid. {e}", 400)

        # Construct the metadata for saving
        metadata_4_save = construct_metadata_4_save(
            metadata, code_path, weight_path, model
        )

        # Save the model's metadata to the database
        try:
            RServer.get_model_wrapper().create_model(metadata_4_save)
        except Exception as e:
            traceback.print_exc()
            clear_model_temp_files(code_path, weight_path)
            return RResponse.fail(f"Failed to save the model. {e}", 400)

        # Set the current model to the newly uploaded model
        RServer.get_model_wrapper().set_current_model(metadata.get("nickname"))

        return RResponse.ok("Success")
    except Exception as e:
        traceback.print_exc()
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
    try:
        return RResponse.ok(
            [model.as_dict() for model in RServer.get_model_wrapper().list_models()]
        )
    except Exception as e:
        traceback.print_exc()
        return RResponse.abort(500, f"Failed to list all models. {e}")
