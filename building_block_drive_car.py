#!/usr/bin/python

from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import explorerhat
import datetime
import sys, tty, termios
from sklearn.externals import joblib
import numpy as np

import image_operations

# Load the model
clf = joblib.load('model.pkl')
#scaler = joblib.load('scaler.pkl')

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

def do_driving(result):
    if result == "left":
        turn_left()
    elif result == "right":
        turn_right()
    elif result == "forward":
        move_forward()

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # Crop, blur, select blue channel, and binarise the image
    processed_image = image_operations.process_image(image)
    processed_image = cv2.resize(processed_image, (24, 24))
    #processed_image = image
    #processed_image = processed_image[240:480, 0:640]
    #processed_image = cv2.blur(processed_image, (5, 5))
    #b,g,r = cv2.split(processed_image)
    #processed_image = b
    #retval, processed_image = cv2.threshold(processed_image, 140, 255, cv2.THRESH_BINARY)

    image_as_array = np.ndarray.flatten(np.array(processed_image))
    result = clf.predict([image_as_array])[0]

    do_driving(result)

    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)

#    fd = sys.stdin.fileno()
#    old_settings = termios.tcgetattr(fd)
#    try:
#        tty.setraw(sys.stdin.fileno())
#        key = sys.stdin.read(1)
#    finally:
#        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#
#    print("Read key %s" % key)
#
#    if key == "q": # if the `q` key was pressed, break from the loop
#        break
#
#    time.sleep(0.5) # Let the car settle to prevent blurring

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
