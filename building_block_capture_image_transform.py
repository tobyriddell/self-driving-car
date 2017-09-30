#!/usr/bin/python

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.vflip = True
camera.color_effects = (128,128) # turn camera to black and white
rawCapture = PiRGBArray(camera, size=(640, 480))
 
# allow the camera to warmup
time.sleep(0.1)
 
## grab an image from the camera
#camera.capture(rawCapture, format="bgr")
#image = rawCapture.array
# 
## display the image on screen and wait for a keypress
#cv2.imshow("Image", image)
#cv2.waitKey(0)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # Blur image and resize
#    image = cv2.resize(image, (25, 25))
#    image = cv2.resize(image, (100, 100))
    image = cv2.blur(image, (5, 5))
    retval, image = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY)
    
    # show the frame
    cv2.imshow("Frame", image)
    key = cv2.waitKey(1) & 0xFF
    
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break
