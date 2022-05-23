from flask import request

from objects.RResponse import RResponse
from objects.RServer import RServer

app = RServer.getServer().getFlaskBluePrint()

@app.route('/config', methods=['GET'])
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
                batch_size: 16,
                device: cpu,
                image_padding: short_side,
                image_size: 32,
                model_arch: resnet-18-32x32,
                num_classes: 10,
                num_workers: 8,
                pre_trained: false,
                shuffle: true,
                weight_to_load: resnet-34.pth
              }
            msg:
              type: string
              example: Success
    """
    # Return server configs to the client
    print("DEBUG: Fetching configs...")
    try:
        configs = RServer.getServerConfigs()
        return RResponse.ok(configs)
    except:
        return RResponse.fail("Failed", -1)
