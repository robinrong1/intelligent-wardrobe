import cv2
import mediapipe as mp
import numpy as np
import base64

# TODO: Have not chosen type for clothing yet
def edit_frame_for_clothing(frame, clothes):
    return perform_frame_manipulation(frame, clothes)

# Initialize MediaPipe Pose solution
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=1)

# Load t-shirt and pants images (transparent PNGs)
tshirt_img = cv2.imread('./clothes/blue.png', cv2.IMREAD_UNCHANGED)  # Ensure it's a transparent PNG
pants_img = cv2.imread('./clothes/pant.png', cv2.IMREAD_UNCHANGED)  # Ensure it's a transparent PNG

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

# Helper function to overlay and skew/stretch the pants on the frame with full lower body coverage
def overlay_and_skew_pants_full_coverage(frame, landmarks, pants_img, width_factor=5, height_factor=1.5):
    if len(landmarks) < 2:  # Check for at least two points (hips and ankles)
        return frame
    
    # Get positions of the hips and ankles from pose landmarks
    left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
    right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
    left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
    right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

    # Calculate hip width
    hip_width = np.linalg.norm(np.array(left_hip) - np.array(right_hip))
    
    # Calculate the oversized width and height for the pants
    oversized_hip_width = hip_width * width_factor
    oversized_height = np.linalg.norm(np.array(left_hip) - np.array(left_ankle)) * height_factor

    # Define the four points to match the oversized pants: top left, top right (hips) and bottom left, bottom right (ankles)
    pants_points = np.array([
        [0, 0],  # Top-left corner of the pants image
        [pants_img.shape[1], 0],  # Top-right corner
        [0, pants_img.shape[0]],  # Bottom-left corner
        [pants_img.shape[1], pants_img.shape[0]]  # Bottom-right corner
    ], dtype=np.float32)

    # Define the points on the frame (human body) to map the pants to: oversized hips and ankles
    body_points = np.array([
        [left_hip[0] - oversized_hip_width // 2, left_hip[1]],  # Extended left hip
        [right_hip[0] + oversized_hip_width // 2, right_hip[1]],  # Extended right hip
        [left_ankle[0] - oversized_hip_width // 2, left_ankle[1] + oversized_height // 3],  # Extended left ankle
        [right_ankle[0] + oversized_hip_width // 2, right_ankle[1] + oversized_height // 3]  # Extended right ankle
    ], dtype=np.float32)
    
    # Calculate the perspective transform matrix
    matrix = cv2.getPerspectiveTransform(pants_points, body_points)

    # Warp the pants image to match the oversized body landmarks (hips and ankles)
    pants_warped = cv2.warpPerspective(pants_img, matrix, (frame.shape[1], frame.shape[0]))

    # Overlay the warped pants on the frame, handling transparency (alpha blending)
    alpha_channel = pants_warped[:, :, 3] / 255.0  # Assuming the 4th channel is alpha
    for y in range(pants_warped.shape[0]):
        for x in range(pants_warped.shape[1]):
            if alpha_channel[y, x] > 0:  # Only blend where the pants are visible
                frame[y, x] = alpha_channel[y, x] * pants_warped[y, x, :3] + (1 - alpha_channel[y, x]) * frame[y, x]

    return frame

def data_url_to_mat(data_url):
    # Step 1: Extract the base64 data from the data URL
    
    base64_data = data_url.split("data:image/png;base64,")[1]
    
    # Step 2: Decode the base64 data to binary data
    binary_data = base64.b64decode(base64_data)
    
    # Step 3: Convert the binary data to a NumPy array
    np_array = np.frombuffer(binary_data, dtype=np.uint8)
    
    # Step 4: Decode the NumPy array to an OpenCV image
    mat = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
    
    return mat

def mat_to_data_url(mat):
    # Step 1: Convert the OpenCV image to binary data
    _, buffer = cv2.imencode(".png", mat)
    
    # Step 2: Encode the binary data to base64
    base64_data = base64.b64encode(buffer).decode('utf-8')

    # Step 3: Combine the base64 data with the data URL prefix
    data_url = f"data:image/png;base64,{base64_data}"
    
    return data_url

def perform_frame_manipulation(frame: cv2.typing.MatLike, clothes):
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
        
        # Skew and stretch the pants to fit the body (hips and ankles) with full lower body coverage
        frame = overlay_and_skew_pants_full_coverage(frame, landmarks, pants_img, width_factor=5, height_factor=1.2)

    else:
        print("No pose landmarks detected.")
        

    return frame


# Update the visualization function to skew/stretch both the t-shirt and pants for full coverage
def visualize_pose_landmarks_with_full_coverage_tshirt_and_pants():
    # Open a video capture using the webcam
    cap = cv2.VideoCapture(0)  # '0' means the default webcam
    
    while cap.isOpened():
        success, frame = cap.read()  # Read a frame from the webcam
        
        if not success:
            print("Ignoring empty camera frame.")
            continue
        
        perform_frame_manipulation(frame, None)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()  # Release the webcam resource
    cv2.destroyAllWindows()  # Close all OpenCV windows

if __name__ == "__main__":
    # Run the live visualization with skewed oversized t-shirt and pants
    visualize_pose_landmarks_with_full_coverage_tshirt_and_pants()

    # Cleanup: Close the MediaPipe instance when done
    pose.close()
