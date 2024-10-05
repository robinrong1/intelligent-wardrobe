import cv2
import numpy as np
from process import find_marker_on_person, overlay_clothes, cleanup

def visualize_pose_landmarks_live():
    # Open a video capture using the webcam
    cap = cv2.VideoCapture(0)  # '0' means the default webcam
    
    while cap.isOpened():
        success, frame = cap.read()  # Read a frame from the webcam
        
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Find pose landmarks
        markers = find_marker_on_person(frame)

        # Overlay the T-shirt on the frame
        frame_with_clothes = overlay_clothes(frame, markers)

        # Draw landmarks on the image if they exist
        if markers:
            mp_drawing = mp.solutions.drawing_utils
            mp_drawing_styles = mp.solutions.drawing_styles
            
            # Decode the markers to draw them
            decoded_markers = [tuple(map(int, marker.decode().split(','))) for marker in markers]

            # Draw the pose landmarks on the frame
            mp_drawing.draw_landmarks(
                frame_with_clothes,
                decoded_markers,
                mp.solutions.pose.POSE_CONNECTIONS,  # Draw connections between landmarks
                landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style()
            )

        # Show the frame with landmarks and T-shirt overlay
        cv2.imshow('Live Pose Detection', frame_with_clothes)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    cap.release()  # Release the webcam resource
    cv2.destroyAllWindows()  # Close all OpenCV windows
    cleanup()  # Cleanup MediaPipe resources

# Run the live visualization
visualize_pose_landmarks_live()
