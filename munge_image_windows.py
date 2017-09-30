import os
import cv2
import numpy as np

path = 'C:\\Users\\toby\\Downloads\\self-driving-car\\training_images_3'

os.chdir(path)

img = cv2.imread("training_image_1502733794000_left.png")
img = img[240:480, 0:640]

img = cv2.blur(img, (5, 5))
b,g,r = cv2.split(img)

img = b

retval, img = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)

cv2.imshow("Image", img)
