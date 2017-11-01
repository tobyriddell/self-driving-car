# self-driving-car

## Summary
A project for Fern School's STEM club to help students get to grips with neural networks

## Introduction

This project was inspired by https://medium.com/@florianherrengt/building-a-basic-self-driving-rc-car-bca6a7521753, 
however there are some differences: I used a Raspberry Pi and a robot car chassis and all code was written in Python and executed
on the Raspberry Pi.

The goal was to lay the groundwork for grade 7/8 students to implement a self-driving car themselves, hence the Python scripts
are in separate files demonstrating the capturing of images, the processing of images, training the neural network and then using
the trained network to drive the car.

## Building blocks:

* Move forwards: building_block_move_forwards.py
* Turn left/right: building_block_turn_left.py, building_block_turn_right_on_spot.py
* Capture images: building_block_capture_image.py
* Transform images: building_block_capture_image_transform.py
* Respond to commands, include command in image name: building_block_lrf_image_capture.py
* Train neural network from captured images: building_block_train_from_images.py
* Use trained neural network to drive car: building_block_drive_car.py

I figured I'd simplify the job of the neural network by cropping the images and filtering out anything that is not blue (the masking tape that I used to lay out the 'road' was blue so this was the key feature the neural network should pay attention to). I'm not sure if this filtering is necessary... I should try again with unfiltered images.

## Examples of raw and processed images:

![Raw image](/sample_images/training_image_raw_forward_1503842519000.png?raw=true "Raw image")
![Processed image](/sample_images/training_image_processed_forward_1503842519000.png?raw=true "Processed image")

Video of the car in action: https://www.youtube.com/watch?v=_Bs-3v7ODe8

<a href="http://www.youtube.com/watch?feature=player_embedded&v=_Bs-3v7ODe8" target="_blank"><img src="http://img.youtube.com/vi/_Bs-3v7ODe8/0.jpg" 
alt="self-driving car in action" width="240" height="180" border="10" /></a>

(Since the video was made the code was updated to move continuously, without needing the Return key pressed.)

Next steps:

* Try training the neural net with unprocessed images
* Switch from a forward/left/right movement model to a velocity-based model. Decisions will update the target velocity rather than explicit movement steps, this should result in smoother motion and the opportunity to speed up/slow down rather than move at constant speed.
* Implement a web server (as per the medium.com article) so that the captured/processed images may be viewed as the car is trained and drives itself.
