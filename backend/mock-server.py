from flask import Flask, request, jsonify
from flask_socketio import SocketIO

app = Flask(__name__)

socketio = SocketIO(app)

@socketio.on('message')
def handle_message(data):
    pass

if __name__ == '__main__':
    socketio.run(app)