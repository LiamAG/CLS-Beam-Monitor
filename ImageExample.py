import cv2
import numpy as np
import epics
import csv
import os.path
import transform
import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from datetime import datetime
from timeit import default_timer as timer
from epics import PV


def file_made(event):
    print(f"New image, {event.src_path} has been detected. Running processing/analysis.")
    start = timer()
    time.sleep(0.01)  # necessary delay to allow the OS to fully place the file in the directory
    new_image_string = f"{event.src_path}"
    print(new_image_string)
    img = cv2.imread(f'{event.src_path}', 0)
    background_img = cv2.imread('background.png', 0)

    background_sub = True
    gaussian_smooth = True
    angle_correct = False
    map_colours = True
    draw_centroid_std_devs = True

    if background_sub:
        img = transform.brightness_difference(img, background_img)
        print("Saving image as output_subtraction.png.")
        cv2.imwrite('./Data/output_subtraction.png', img)

    if angle_correct:  # Uses a set of 4 pre-defined points to generate a rectangular ROI
        pts = np.float32(
            [[1849, 912], [2845, 882], [2889, 1880], [1887, 1918]])  # Point set for the printed target test image
        img = transform.perspective_transform(img, pts)
        print("Saving image as distortion_output.png.")
        cv2.imwrite('./Data/output_distortion.png', img)

    if gaussian_smooth:
        img = cv2.GaussianBlur(img, (5, 5), 0)
        print("Saving image as output_smoothed.png.")
        cv2.imwrite('./Data/output_smoothed.png', img)

    # end of processing, start analysis functions:

    M = cv2.moments(img)
    centroidX = int(M["m10"] / M["m00"])
    centroidY = int(M["m01"] / M["m00"])
    stddevX = np.sqrt(int(M["mu20"] / M["m00"]))
    stddevY = np.sqrt(int(M["mu02"] / M["m00"]))
    print("Coordinates of centroid (X,Y): ", centroidX, " ", centroidY)
    print("Std. dev: (X,Y): ", stddevX, " ", stddevY)

    modified_img = img  # apply filters/overlays to the processed image without losing it

    if map_colours:
        modified_img = cv2.applyColorMap(modified_img, cv2.COLORMAP_JET)
        print("Saving image as output_false_colour.png.")
        cv2.imwrite('./Data/output_false_colour.png', modified_img)

    if draw_centroid_std_devs:
        modified_img = cv2.circle(modified_img, (centroidX, centroidY), 20, (255, 102, 255),
                                  3)  # plots the centroid as a circle

        modified_img = cv2.line(modified_img, (centroidX + int(stddevX), centroidY + 30),
                                (centroidX + int(stddevX), centroidY - 30), (255, 102, 255),
                                3)  # plots the first standard deviation from the centroid in x and y
        modified_img = cv2.line(modified_img, (centroidX - int(stddevX), centroidY + 30),
                                (centroidX - int(stddevX), centroidY - 30), (255, 102, 255), 3)
        modified_img = cv2.line(modified_img, (centroidX + 30, centroidY + int(stddevY)),
                                (centroidX - 30, centroidY + int(stddevY)), (255, 102, 255), 3)
        modified_img = cv2.line(modified_img, (centroidX + 30, centroidY - int(stddevY)),
                                (centroidX - 30, centroidY - int(stddevY)), (255, 102, 255), 3)

        modified_img = cv2.line(modified_img, (centroidX + 2 * int(stddevX), centroidY + 30),
                                (centroidX + 2 * int(stddevX), centroidY - 30), (255, 102, 255),
                                3)  # plots the second standard deviation from the centroid in x and y
        modified_img = cv2.line(modified_img, (centroidX - 2 * int(stddevX), centroidY + 30),
                                (centroidX - 2 * int(stddevX), centroidY - 30), (255, 102, 255), 3)
        modified_img = cv2.line(modified_img, (centroidX + 30, centroidY + 2 * int(stddevY)),
                                (centroidX - 30, centroidY + 2 * int(stddevY)), (255, 102, 255), 3)
        modified_img = cv2.line(modified_img, (centroidX + 30, centroidY - 2 * int(stddevY)),
                                (centroidX - 30, centroidY - 2 * int(stddevY)), (255, 102, 255), 3)
        print("Saving image as output_false_colour_centroid.png.")
        cv2.imwrite('./Data/output_false_colour_centroid_std_devs.png', modified_img)

    # end of analysis - begin saving results

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    current_date = now.strftime("%Y-%m-%d")

    csv_exists = os.path.isfile('./Data/' + current_date + '_outputData.csv')  # checks if CSV for today exists.
    with open('./Data/' + current_date + '_outputData.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if csv_exists is False:  # writes in the header if the CSV is new and has no data in it
            writer.writerow(['Time', 'Centroid X', 'Centroid Y', 'Std Dev X', 'Std Dev Y'])
        writer.writerow([current_time, centroidX, centroidY, stddevX, stddevY])

    end = timer()
    print("Elapsed time:", end - start, "seconds")


if __name__ == "__main__":
    patterns = "*.png"  # only checks results of these filetypes
    ignore_patterns = "*.csv", "*.jpg"  # presumably unnecessary, but deliberately avoids these filetypes!
    ignore_directories = True
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    event_handler.on_created = file_made
    path = "."
    observer = Observer()
    observer.schedule(event_handler, path, recursive=False)  # recursive determines if subdirectories will be searched
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

