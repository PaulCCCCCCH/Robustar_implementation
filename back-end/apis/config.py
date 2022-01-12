from flask import request

from objects.RResponse import RResponse
from objects.RServer import RServer

app = RServer.getServer().getFlaskApp()

@app.route('/config', methods=['GET'])
def get_config():
    # Return server configs to the client
    print("DEBUG: Fetching configs...")
    try:
        configs = RServer.getServerConfigs()
        return RResponse.ok(configs)
    except:
        return RResponse.fail("Failed", -1)
