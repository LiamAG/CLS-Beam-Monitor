import cv2
import numpy as np
import epics
import transform
from timeit import default_timer as timer
import inotify as i
import sys


def diff_image(background, image, output_dir):
    diffed_img = transform.brightness_difference(image, background)
    return diffed_img


def map_false_colour(image, output_dir=None):
    false_colour = cv2.applyColorMap(image, cv2.COLORMAP_JET)
    return false_colour

def get_moments(image):
    M = cv2.moments(image)
    return M


def centroid(image):
    M = get_moments(image)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    print("Coordinates of centroid (X,Y): ", cX, " ", cY)
    image = map_false_colour(image)
    image = cv2.circle(image, (cX, cY), 20, (255, 102, 255), 3)
    return image

def std_devs(image, M):
    M = get_moments(image)
    centroidX = int(M["m10"] / M["m00"])
    centroidY = int(M["m01"] / M["m00"])
    stddevX = np.sqrt(int(M["mu20"] / M["m00"]))
    stddevY = np.sqrt(int(M["mu02"] / M["m00"]))
    image = cv2.line(image, (centroidX + int(stddevX), centroidY + 30), (centroidX + int(stddevX), centroidY - 30), (255, 102, 255), 3)
    image = cv2.line(image, (centroidX - int(stddevX), centroidY + 30), (centroidX - int(stddevX), centroidY - 30), (255, 102, 255), 3)
    image = cv2.line(image, (centroidX + 30, centroidY + int(stddevY)), (centroidX - 30, centroidY + int(stddevY)), (255, 102, 255), 3)
    image = cv2.line(image, (centroidX + 30, centroidY - int(stddevY)), (centroidX - 30, centroidY - int(stddevY)), (255, 102, 255), 3)

    image = cv2.line(image, (centroidX + 2*int(stddevX), centroidY + 30), (centroidX + 2*int(stddevX), centroidY - 30), (255, 102, 255), 3)
    iamge = cv2.line(image, (centroidX - 2*int(stddevX), centroidY + 30), (centroidX - 2*int(stddevX), centroidY - 30), (255, 102, 255), 3)
    image = cv2.line(image, (centroidX + 30, centroidY + 2*int(stddevY)), (centroidX - 30, centroidY + 2*int(stddevY)), (255, 102, 255), 3)
    image = cv2.line(image, (centroidX + 30, centroidY - 2*int(stddevY)), (centroidX - 30, centroidY - 2*int(stddevY)), (255, 102, 255), 3)
    return image

if __name__ == "__main__":

    background_sub = True
    map_colours = True
    draw_centroid = True
    draw_std_devs = True


