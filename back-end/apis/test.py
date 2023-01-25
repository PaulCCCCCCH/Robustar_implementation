from flask import request

from objects.RResponse import RResponse
from objects.RServer import RServer
from utils.test import start_test
from flask import Blueprint

test_api = Blueprint("test_api", __name__)


@test_api.route("/test", methods=["POST"])
def start_testing():
    """
    Starts the test thread
    ---
    tags:
      - test
    consumes:
      - "application/json"
    produces:
      - "application/json"
    parameters:
      - in: "body"
        name: "body"
        description: "The split to test, valid values: 'test' or 'validation'"
        required: true
        schema:
          properties:
            split:
              type: string
              example: test
    responses:
      200:
        description: Test started or test cannot be started
        schema:
          properties:
            code:
              type: integer
              example: 0
            data:
              type: string
              example: Test started!
            msg:
              type: string
              example: Success
    """
    # print("DEBUG: Testing request received! ...")

    json_data = request.get_json()
    split = json_data["split"]
    if split not in ["validation", "test"]:
        RResponse.abort(400, "Wrong split chosen for test")
    # print(split)

    try:
        start_test(split)
    except Exception as e:
        RResponse.abort(500, "Failed to start testing - " + str(e))

    return RResponse.ok("Test started")
