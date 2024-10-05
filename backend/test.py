from process import edit_frame_for_clothes
import cv2

# Initialize video capture
capture = cv2.VideoCapture(0)

# edit this until we stop
while True:
    ret, frame = capture.read()
    
    # If we don't get a frame, break
    if not ret:
        break
    
    # TODO: Add the clothes to the frame
    new_frame = edit_frame_for_clothes(frame, None)

    cv2.imshow('frame', new_frame)