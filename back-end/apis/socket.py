from objects.RServer import RServer
from objects.RResponse import RResponse
from flask_socketio import emit

server = RServer.getServer()
socketio = RServer.getSocket()

@socketio.on('connect')
def test_connect():
    print("Successfully connected to frontend with socket")
    emit('afterConnect',  {'data':'Lets dance'})

# @socketio.on('message')
# def handle_message(data):
#     print('received message: ' + data)

# @socketio.on('json')
# def handle_json(json):
#     print('received json: ' + str(json))

# @socketio.on('my event')
# def handle_my_custom_event(json):
#     print('received json: ' + str(json))

# @socketio.on('my_event')
# def handle_my_custom_event(arg1, arg2, arg3):
#     print('received args: ' + arg1 + arg2 + arg3)