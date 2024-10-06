from process import edit_frame_for_clothing, data_url_to_mat
from flask import Flask, render_template, Response, request
from flask_cors import CORS
from queue import Queue
import cv2

app = Flask(__name__)
CORS(app)  # Add this line to enable CORS

def select_clothing(sid, data):
    pass

def prompt_suggestions(sid, data):
    pass

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)