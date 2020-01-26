import cv2
import numpy as np
import epics
import transform
from timeit import default_timer as timer
import inotify.adapters
import sys


def diff_image(background, image):
    diffed_img = transform.brightness_difference(image, background)
    return diffed_img


def smooth_image(image):
    diffed_img = cv2.GaussianBlur(image, (5, 5), 0) #smoothing is a function of these values. potentially worth changing?
    return smooth_image


def map_false_colour(image):
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


def std_devs(image):
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

    if len(sys.argv) != 3:
        sys.exit("Only watched directory and output directory should be included as input")
    directory = sys.argv[1]
    output_dir = sys.argv[2]  # Save processed images in a new directory for now, can save as EPICS PVs in production
    # Hardcode processing layer booleans for now
    # Hopefully these will pull from EPICS PVs in production
    background_sub = True
    gaussian_smooth = True
    map_colours = True
    draw_centroid = True
    draw_std_devs = True
    background_image_filepath = "Stephen change this to your background image file"
    
    # Create inotify adapter and add a watch on target image directory
    i = inotify.adapters.Inotify()
    i.add_watch(directory)

    while True:
        for event in i.event_gen(yield_nones=False):
            (_, type_names, path, filename) = event
            logger.debug(event)
            # When a png file is created or moved to the directory, begin processing
            if ("png" in filename) and (("IN_CLOSE_WRITE" in type_names) or ("IN_MOVED_TO" in type_names)):
                # I will probably get the file naming wrong, play with it until it works on your end
                # for now I'll just use filename to represent the image file
                image = cv2.imread(filename)
                background = cv2.imread(background_image_filepath)

                # Run processing functions
                if background_sub:
                    image = diff_image(background, image)
                if gaussian_smooth:
                    image = smooth_image(image)
                if map_colours:
                    image = map_false_colour(image)
                if draw_centroid:
                    image = centroid(image)
                if draw_std_devs:
                    image = std_devs(image)

                print("Saving processed image in", output_dir)
                cv2.imwrite(output_dir+ "/processed_" + filename)
