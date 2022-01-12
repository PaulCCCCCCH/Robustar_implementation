from flask import request

from objects.RResponse import RResponse
from objects.RServer import RServer

app = RServer.getServer().getFlaskApp()

@app.route('/config', methods=['GET'])
def get_config():
    # Try to start training thread
    print("DEBUG: Fetching configs...")
    try:
        configs = RServer.getServerConfigs()
        # print(split)
        return RResponse.ok(configs)
    except:
        return RResponse.fail("Failed", -1)
