from process import edit_frame_for_clothing, set_clothing
from prompting_service import prompt_user
from flask import Flask, render_template, Response, request, jsonify, send_from_directory
from flask_cors import CORS
from queue import Queue
import os
import cv2

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS

@app.route('/select-clothing', methods=['POST'])
def select_clothing():
    data = request.json
    print(data)
    set_clothing(data)
    return Response(status=200)

@app.route('/list-clothing')
def list_clothing():
    wardrobe = os.listdir('./Clothes')
    clothes = []
    for i, item in enumerate(wardrobe):
        clothes.append(item.split('.')[0])
    return jsonify({ 'clothes': clothes })

@app.route('/clothes/<file>')
def clothes():
    return send_from_directory('Clothes', f'${request.view_args["file"]}.png')

@app.route('/add-clothes', methods=['POST'])
def add_clothes():
    file = request.files['file']  # Get the uploaded file
    if file:
        # Save the file in the 'Clothes' folder
        file.save(os.path.join('./Clothes', file.filename))
        # Return the filename so the frontend can update its state
        return jsonify({'status': 'success', 'filename': file.filename}), 200
    return jsonify({'status': 'error', 'message': 'No file uploaded'}), 400


def generate_frames():
    # Open a video capture using the webcam
    cap = cv2.VideoCapture(0)  # '0' means the default webcam
    
    while cap.isOpened():
        success, frame = cap.read()  # Read a frame from the webcam
        
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        new_frame = edit_frame_for_clothing(frame, None)
        img_str = cv2.imencode('.jpg', new_frame)[1].tostring()
        
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + img_str + b'\r\n')

        # Break the loop when 'q' is pressed
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()  # Release the webcam resource
    cv2.destroyAllWindows()  # Close all OpenCV windows
    

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/prompt', methods=['POST'])
def prompt():
    data = request.json
    message = data['message']
    
    list = []
    for i in range(3):
        response0 = prompt_user(message)
        for i in response0.split(', '):
            if i not in list:
                list.append(i)
    
    return jsonify({ 'clothes': list })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)