import cv2
import numpy as np
import epics
import transform
from timeit import default_timer as timer
import inotify as i


def diff_image(background, image, output_dir):
    diffed_img = transform.brightness_difference(image, background)
    print("Saving image as subtraction_output.png.")
    cv2.imwrite(output_dir + 'output_subtraction.png', diffed_img)
    return diffed_img


def false_colour(image, output_dir=None):
    false_colour = cv2.applyColorMap(image, cv2.COLORMAP_JET)
    print("Saving image as false_colour_output.png.")
    if output_dir:
        cv2.imwrite(output_dir + 'output_false_colour.png', false_colour)
    return false_colour


def centroid(image, output_dir):
    M = cv2.moments(image)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    print("Coordinates of centroid (X,Y): ", cX, " ", cY)
    false_colour = false_colour(image)
    false_colour_centroid = cv2.circle(false_colour, (cX, cY), 20, (255, 102, 255), 3)
    print("Saving image as output_false_colour_centroid.png.")
    cv2.imwrite(output_dir + 'output_false_colour_centroid.png', false_colour_centroid)
    return
