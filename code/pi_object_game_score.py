import cv2
from ultralytics import YOLO
import logging
import screeninfo
import time
from picamera2 import Picamera2


#Suppress the ultralytics output
logging.getLogger("ultralytics").setLevel(logging.WARNING)

#Use Screen Example from here: https://gist.github.com/ronekko/dc3747211543165108b11073f929b85e
screen_id = 0
# get the size of the screen
screen = screeninfo.get_monitors()[screen_id]
width, height = screen.width, screen.height

#Setup the full screen window
window_name = 'YoloV8'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,
                          cv2.WINDOW_FULLSCREEN)


#Set up the camera 
cap = Picamera2()
#Little help from Google AI to get the right format 
cap.configure(cap.create_preview_configuration(main={"format": 'RGB888', "size": (640,480)}))
cap.start() 


#Game Score
score = 0 
#How much time to wait between object views to increment the point, in seconds
wait_point = 20
#Init to allow point at startup 
time_since_last_point = time.time() - wait_point 
#Percent confidence we need to be above 
confidence_threshold = 0.2
#Text info 
text_org = (round(height*0.10), round(width*.10))
text_font = cv2.FONT_HERSHEY_SIMPLEX
text_scale = 3
text_color = (0, 255, 0)
text_thickness = 1
# Load the YOLOv8 model
model = YOLO("best.pt")


#Setup the loop 
key = ord("r")
# Loop through the video frames
while key != ord("s"):
    # Read a frame from the video
    success = True
    frame = cap.capture_array()

    if success:
        # Run YOLOv8 inference on the frame
        results = model(frame, verbose=False)
        # Visualize the results on the frame
        annotated_frame = results[0].plot()
        #Get the confidence for class 0 (object) (help from stack overflow)
        confidence = results[0].boxes.conf.tolist()
        #Get the first max value if the list is not empty  
        if confidence != []:
            confidence = max(confidence)
            #If we are confident it was identified correctly 
            if confidence > confidence_threshold:
                curr_time = time.time()
                #If we are beyond the wait for the next point - increment the 
                #score and then reset 
                if curr_time - time_since_last_point > wait_point:
                    time_since_last_point = curr_time
                    score += 1
        #Resize 
        annotated_frame = cv2.resize(annotated_frame, (width, height))
        #Display the score
        display_text = f"Score: {score}" 
        annotated_frame = cv2.putText(annotated_frame, display_text,
                                    text_org, text_font, text_scale, text_thickness,
                                    cv2.LINE_AA)
        
        # Display the annotated frame
        cv2.imshow(window_name, annotated_frame)
        key = cv2.waitKey(10)
    else:
        print("No successful read")
        