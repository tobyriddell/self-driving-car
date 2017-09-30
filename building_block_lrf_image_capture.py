#!/usr/bin/python

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import explorerhat
import datetime
import sys, tty, termios
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
camera.vflip = True
#camera.color_effects = (128,128) # turn camera to black and white
rawCapture = PiRGBArray(camera, size=(640, 480))
# allow the camera to warmup
time.sleep(0.1)

def turn_left():
    explorerhat.motor.two.forward(100)
    time.sleep(0.5)
    explorerhat.motor.two.stop()

def turn_right():
    explorerhat.motor.one.forward(100)
    time.sleep(0.5)
    explorerhat.motor.one.stop()

def move_forward():
    explorerhat.motor.forwards()
    time.sleep(0.5)
    explorerhat.motor.stop()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # Blur image and resize
#    image = cv2.resize(image, (25, 25))
#    image = cv2.resize(image, (100, 100))
    #image = cv2.blur(image, (5, 5))
    #retval, image = cv2.threshold(image, 140, 255, cv2.THRESH_BINARY)
    
    # show the frame
    #cv2.imshow("Frame", image)
    #key = cv2.waitKey(1) & 0xFF
    #key = cv2.waitKey(0) & 0xFF

    # Crop, blur, select blue channel, and binarise the image
    processed_image = image
    processed_image = processed_image[240:480, 0:640]
    processed_image = cv2.blur(processed_image, (5, 5))

    processed_image_hsv = cv2.cvtColor(processed_image, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100,50,50])
    upper_blue = np.array([130,255,255])

    mask = cv2.inRange(processed_image_hsv, lower_blue, upper_blue)
    processed_image_masked = cv2.bitwise_and(processed_image, processed_image, mask=mask)

    # Get human input to decide next course of action
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        key = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    print("Read key %s" % key)

    if key == "a":
        filename = "training_image_raw_left_%d.png" % (int(datetime.datetime.now().strftime("%s")) * 1000 )
        processed_filename = "training_image_processed_left_%d.png" % (int(datetime.datetime.now().strftime("%s")) * 1000 )
        turn_left()
    elif key == "d":
        filename = "training_image_raw_right_%d.png" % (int(datetime.datetime.now().strftime("%s")) * 1000 )
        processed_filename = "training_image_processed_right_%d.png" % (int(datetime.datetime.now().strftime("%s")) * 1000 )
        turn_right()
    elif key == "w":
        filename = "training_image_raw_forward_%d.png" % (int(datetime.datetime.now().strftime("%s")) * 1000 )
        processed_filename = "training_image_processed_forward_%d.png" % (int(datetime.datetime.now().strftime("%s")) * 1000 )
        move_forward()
    elif key == "q": # if the `q` key was pressed, break from the loop
        break

    # Save raw image to file
    cv2.imwrite(filename, image)

    # Save processed image to file
    cv2.imwrite(processed_filename, processed_image_masked)

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

    time.sleep(0.5) # Let the car settle to prevent blurring

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
