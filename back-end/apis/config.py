from flask import request

from objects.RResponse import RResponse
from objects.RServer import RServer
from flask import Blueprint

config_api = Blueprint("config_api", __name__)


@config_api.route("/config", methods=["GET"])
def get_config():
    """
    Gets current server configuration
    ---
    tags:
      - config
    produces:
      - "application/json"
    responses:
      200:
        description: Server configuration
        schema:
          properties:
            code:
              type: integer
              example: 0
            data:
              type: object
              example: {
                device: cpu,
                image_padding: short_side,
                image_size: 32,
                num_classes: 10,
              }
            msg:
              type: string
              example: Success
    """
    # Return server configs to the client
    print("DEBUG: Fetching configs...")
    try:
        configs = RServer.get_server_configs()
        return RResponse.ok(configs)
    except Exception as e:
        RResponse.abort(500, f"Cannot retrieve server configs. ({e})", -1)
