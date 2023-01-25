from objects.RServer import RServer
from objects.RResponse import RResponse
from flask_socketio import emit

server = RServer.get_server()
socketio = RServer.get_socket()


@socketio.on("connect")
def test_connect():
    print("Successfully connected to frontend with socket")
    emit("afterConnect", {"data": "Lets dance"})
