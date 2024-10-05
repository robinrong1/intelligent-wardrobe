from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from process import edit_frame_for_clothing

app = Flask(__name__)
socketio = SocketIO(app)

@socketio.on('process_frame')
def process_frame(data):
    video_frame = edit_frame_for_clothing(data.frame, None)
    emit('video_frame', video_frame, to=request.sid)
    
@socketio.on('select_clothing')
def select_clothing(data):
    pass
    
@socketio.on('prompt_suggestions')
def prompt_suggestions(data):
    pass

if __name__ == '__main__':
    socketio.run(app)