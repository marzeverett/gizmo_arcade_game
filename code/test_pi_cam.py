import cv2
import logging
import screeninfo
import time
from picamera2 import Picamera2



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


#Setup the loop 
key = ord("r")
# Loop through the video frames
while key != ord("s"):
    # Read a frame from the video
    success = True
    frame = cap.capture_array()

    if success:
        annotated_frame = frame 
        # Display the annotated frame
        cv2.imshow(window_name, annotated_frame)
        key = cv2.waitKey(10)
    else:
        print("No successful read")
        