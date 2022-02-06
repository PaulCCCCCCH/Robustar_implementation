from objects.RServer import RServer
from objects.RResponse import RResponse
from flask_socketio import emit

app = RServer.getServer().getFlaskApp()
server = RServer.getServer()
socketio = RServer.getSocket()

@socketio.on('connect')
def test_connect():
    emit('after connect',  {'data':'Lets dance'})