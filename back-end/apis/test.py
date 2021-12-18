from flask import request

from objects.RResponse import RResponse
from objects.RServer import RServer
from utils.test import start_test

app = RServer.getServer().getFlaskApp()


@app.route('/test', methods=['POST'])
def start_testing():
    # Try to start training thread
    print("DEBUG: Testing request received! ...")

    json_data = request.get_json()
    split = json_data['split']
    # print(split)

    test_thread = start_test(split)

    if not test_thread:
        return RResponse.fail("Failed", -1)

    return RResponse.ok("Test started!")
