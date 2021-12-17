from objects.RResponse import RResponse
from objects.RServer import RServer

app = RServer.getServer().getFlaskApp()


@app.route('/test', methods=['POST'])
def start_testing():
    # test_thread = None
    #
    # if not test_thread:
    #     return RResponse.fail("Failed", -1)

    return RResponse.ok("Test started!")
