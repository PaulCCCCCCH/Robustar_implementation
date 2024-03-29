from objects.RServer import RServer
from flask import request
from utils.generate import generate_paired_data
from flask import Blueprint

generate_api = Blueprint("generate_api", __name__)


# Not used by current version
@generate_api.route("/generate", methods=["POST"])
def generate():
    print("Requested to generate paired dataset")
    json_data = request.get_json()

    # TODO: Create a new thread to do this so that it does not block the server.
    generate_paired_data(json_data["mirrored_data_path"], json_data["user_edit_path"])
    return {"msg": "Generation completed!", "code": 0}


if __name__ == "__main__":
    print(generate_paired_data)
