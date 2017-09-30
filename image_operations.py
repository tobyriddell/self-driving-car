import cv2
import numpy as np

def process_image(image):
    # Crop, blur, select blue
    processed_image = image
    processed_image = processed_image[240:480, 0:640]
    processed_image = cv2.blur(processed_image, (5, 5))

    processed_image_hsv = cv2.cvtColor(processed_image, cv2.COLOR_BGR2HSV)

    lower_blue = np.array([100,50,50])
    upper_blue = np.array([130,255,255])

    mask = cv2.inRange(processed_image_hsv, lower_blue, upper_blue)
    processed_image_masked = cv2.bitwise_and(processed_image, processed_image, mask=mask)
    return processed_image_masked
    
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
