#JUST TO STORE THE NODE CREATED FILE HERE!!!
# Imports for finding the node/markers on the person.
import cv2
import mediapipe as mp
import numpy as np
from typing import List, ByteString

from typing import Generator, List, ByteString

# Initialize MediaPipe Pose solution
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1)

# TODO: Have not chosen type for clothing yet
def edit_frame_for_clothes(frames: Generator[List[ByteString], None, None], clothes) -> Generator[List[ByteString], None, None]:
    for frame in frames:
        yield frame

# TODO: Create the markers for the clothers for the pasting
def create_marker_for_clothes(clothes):
    pass

# TODO: Find the markers on the person
def find_marker_on_person(frame: List[ByteString]):
    # Convert the ByteString frame into an image
    image = cv2.imdecode(np.frombuffer(frame, np.uint8), cv2.IMREAD_COLOR)
    
    # Convert the image color to RGB as required by MediaPipe
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Process the image and get pose landmarks
    results = pose.process(image_rgb)
    
    if results.pose_landmarks:
        markers = []
        for landmark in results.pose_landmarks.landmark:
            h, w, _ = image.shape
            x, y = int(landmark.x * w), int(landmark.y * h)
            markers.append((x, y))
        return markers
    else:
        return []

#This logic should stay here just incase if test.py does not work!
'''def visualize_pose_landmarks_live():
    # Open a video capture using the webcam
    cap = cv2.VideoCapture(0)  # '0' means the default webcam
    
    while cap.isOpened():
        success, frame = cap.read()  # Read a frame from the webcam
        
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Convert the image color to RGB (required by MediaPipe)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image to detect pose landmarks
        results = pose.process(image_rgb)
        
        # Draw landmarks on the image if they exist
        if results.pose_landmarks:
            # Draw landmarks directly on the frame using MediaPipe's drawing utility
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles
            
            # Draw the pose landmarks on the frame
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,  # Draw connections between landmarks
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )

        # Show the frame with landmarks
        cv2.imshow('Live Pose Detection', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()  # Release the webcam resource
    cv2.destroyAllWindows()  # Close all OpenCV windows

# Run the live visualization
visualize_pose_landmarks_live()'''

# Cleanup: Close the MediaPipe instance when done
pose.close()

###############################################################################################################################

import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose solution
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1)

# Load t-shirt image (blue.png)
tshirt_img = cv2.imread('blue.png', cv2.IMREAD_UNCHANGED)  # Ensure it's a transparent PNG

# Helper function to overlay and skew/stretch the t-shirt on the frame with full upper body coverage
def overlay_and_skew_tshirt_full_coverage(frame, landmarks, tshirt_img, width_factor=2.7, height_factor=1):
    if len(landmarks) < 2:  # Check for at least two points (shoulders and hips)
        return frame
    
    # Get positions of the shoulders and hips from pose landmarks
    left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value]
    right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value]
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    
    # Approximate chin position by averaging mouth landmarks
    mouth_left = landmarks[mp_pose.PoseLandmark.MOUTH_LEFT.value]
    mouth_right = landmarks[mp_pose.PoseLandmark.MOUTH_RIGHT.value]
    chin = ((mouth_left[0] + mouth_right[0]) // 2, (mouth_left[1] + mouth_right[1]) // 2)  # Approximate chin position

    # Calculate shoulder width and hip width
    shoulder_width = np.linalg.norm(np.array(left_shoulder) - np.array(right_shoulder))
    
    # Calculate the oversized width and height for the shirt
    oversized_shoulder_width = shoulder_width * width_factor
    oversized_height = np.linalg.norm(np.array(chin) - np.array(left_hip)) * height_factor

    # Define the four points to match the oversized t-shirt: top left, top right (shoulders) and bottom left, bottom right (hips)
    tshirt_points = np.array([
        [0, 0],  # Top-left corner of the t-shirt image
        [tshirt_img.shape[1], 0],  # Top-right corner
        [0, tshirt_img.shape[0]],  # Bottom-left corner
        [tshirt_img.shape[1], tshirt_img.shape[0]]  # Bottom-right corner
    ], dtype=np.float32)

    # Define the points on the frame (human body) to map the t-shirt to: oversized shoulders and hips
    body_points = np.array([
        [left_shoulder[0] - oversized_shoulder_width // 2, chin[1]],  # Extended left shoulder to chin
        [right_shoulder[0] + oversized_shoulder_width // 2, chin[1]],  # Extended right shoulder to chin
        [left_hip[0] - oversized_shoulder_width // 2, left_hip[1] + oversized_height // 3],  # Extended left hip
        [right_hip[0] + oversized_shoulder_width // 2, right_hip[1] + oversized_height // 3]  # Extended right hip
    ], dtype=np.float32)
    
    # Calculate the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(tshirt_points, body_points)

    # Warp the t-shirt image to match the oversized body landmarks (shoulders and hips)
    tshirt_warped = cv2.warpPerspective(tshirt_img, matrix, (frame.shape[1], frame.shape[0]))

    # Overlay the warped t-shirt on the frame, handling transparency (alpha blending)
    alpha_channel = tshirt_warped[:, :, 3] / 255.0  # Assuming the 4th channel is alpha
    for y in range(tshirt_warped.shape[0]):
        for x in range(tshirt_warped.shape[1]):
            if alpha_channel[y, x] > 0:  # Only blend where the t-shirt is visible
                frame[y, x] = alpha_channel[y, x] * tshirt_warped[y, x, :3] + (1 - alpha_channel[y, x]) * frame[y, x]

    return frame

# Update the visualization function to skew/stretch the t-shirt to fit the body with full upper body coverage
def visualize_pose_landmarks_with_full_coverage_tshirt():
    # Open a video capture using the webcam
    cap = cv2.VideoCapture(0)  # '0' means the default webcam
    
    while cap.isOpened():
        success, frame = cap.read()  # Read a frame from the webcam
        
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Convert the image color to RGB (required by MediaPipe)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image to detect pose landmarks
        results = pose.process(image_rgb)
        
        # Draw landmarks on the image if they exist
        if results.pose_landmarks:
            # Draw landmarks directly on the frame using MediaPipe's drawing utility
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles
            
            # Draw the pose landmarks on the frame (body nodes - blue and orange)
            mp_drawing.draw_landmarks(
                frame,
                results.pose_landmarks,
                mp_pose.POSE_CONNECTIONS,  # Draw connections between landmarks
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )

            # Get pose landmarks
            landmarks = []
            for landmark in results.pose_landmarks.landmark:
                h, w, _ = frame.shape
                x, y = int(landmark.x * w), int(landmark.y * h)
                landmarks.append((x, y))
            
            # Skew and stretch the t-shirt to fit the body (shoulders and hips) with full upper body coverage
            frame = overlay_and_skew_tshirt_full_coverage(frame, landmarks, tshirt_img, width_factor=2.5, height_factor=1)

        # Show the frame with skewed oversized t-shirt
        cv2.imshow('Live Pose Detection with Full Coverage T-shirt', frame)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()  # Release the webcam resource
    cv2.destroyAllWindows()  # Close all OpenCV windows

# Run the live visualization with skewed oversized t-shirt
visualize_pose_landmarks_with_full_coverage_tshirt()

# Cleanup: Close the MediaPipe instance when done
pose.close()
