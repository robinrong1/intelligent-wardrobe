from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
from process import edit_frame_for_clothing, data_url_to_mat, mat_to_data_url

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", transports=["websocket"])

@socketio.on('connect')
def connect():
    print("Connected!")

@socketio.on('process_frame')
def process_frame(data):
    print("Reached!")
    data_frame = data['frame']
    
    video_frame = edit_frame_for_clothing(data_url_to_mat(data_frame), None)
    
    emit('video_frame', { "url": mat_to_data_url(video_frame) }, to=request.sid)
    print("Finished!")

@socketio.on('hello')
def hello(data):
    print(data['message'])
    emit('hello', { "message": "Hello, Client!" }, to=request.sid)    

@socketio.on('select_clothing')
def select_clothing(data):
    pass
    
@socketio.on('prompt_suggestions')
def prompt_suggestions(data):
    pass

@app.route('/process_frame', methods=['POST'])
def process_frame():
    print("Reached!")
    data = request.json()
    data_frame = data['frame']
    
    video_frame = edit_frame_for_clothing(data_url_to_mat(data_frame), None)
    
    return jsonify({ "url": mat_to_data_url(video_frame) })
    

@app.route('/hello')
def hello():
    return jsonify({ "message": "Hello, Client!" })    

def select_clothing(data):
    pass
    
def prompt_suggestions(data):
    pass

if __name__ == '__main__':
    socketio.run(app)