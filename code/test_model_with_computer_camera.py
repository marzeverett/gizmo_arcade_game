#From here: https://docs.ultralytics.com/modes/predict/#thread-safe-inference

import cv2
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO("best.pt")

# Open the video file

cap = cv2.VideoCapture(0)

key = ord("r")
# Loop through the video frames
while key != ord("s"):
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame)
        
        # Visualize the results on the frame
        annotated_frame = results[0].plot()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Inference", annotated_frame)
        key = cv2.waitKey(5)