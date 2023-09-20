from flask import Blueprint
from objects.RServer import RServer
from objects.RResponse import RResponse

model_api = Blueprint("model_api", __name__)


@model_api.route("/model/current/<model_id>", methods=["POST"])
def api_set_current_model(model_id: str):
    try:
        RServer.get_model_wrapper().set_current_model(model_id)
        return RResponse.ok("Success")
    except Exception as e:
        RResponse.abort(500, "Failed to switch model." + str(e))
