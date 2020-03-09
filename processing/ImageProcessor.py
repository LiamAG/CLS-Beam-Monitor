import cv2
import numpy as np
import matplotlib
import csv
import os.path
import transform
import sys
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from datetime import datetime
from timeit import default_timer as timer



def file_made(event):
    print(f"New image, {event.src_path} has been detected. Running processing/analysis.")
    start = timer()
    time.sleep(0.05)  # necessary delay to allow the OS to fully place the file in the directory
    img = cv2.imread(f'{event.src_path}', 0)
    background_img = cv2.imread('background.png', 0)
    if os.path.isfile('./test_caps/grabbedImage.png'):  # deletes grabbedImage.png - watchdog only triggers on file creations, so if you want it to catch the same file successively (but only once) you need to delete the file once you are done with it
        os.remove('./test_caps/grabbedImage.png')
    original_img = img

    now = datetime.now()
    current_time = now.strftime("%H-%M-%S")
    current_date = now.strftime("%Y-%m-%d")

    outfile = './Captured_Images/' + current_date + '_' + current_time + '.png'   # saves orignal image for archival
    print("Saving image as " + outfile)
    cv2.imwrite(outfile, original_img)
    cv2.imwrite('./Data/original_image.png', img)

    background_sub = True
    gaussian_smooth = False
    angle_correct = True
    map_colours = True
    draw_contours = True
    draw_centroid_std_devs = True

    if background_sub:
        img = transform.brightness_difference(img, background_img)
        print("Saving image as ./Data/output_subtraction.png.")
        cv2.imwrite('./Data/output_subtraction.png', img)

    M = cv2.moments(img)
    if M["m00"] != 0:
        initialcentroidX = int(M["m10"] / M["m00"])
        initialcentroidY = int(M["m01"] / M["m00"])
        initialstddevX = np.sqrt(int(M["mu20"] / M["m00"]))
        initialstddevY = np.sqrt(int(M["mu02"] / M["m00"]))
    else:
        print("Pure black image - no processing has been performed. ")
        return

    if angle_correct:  # Uses a set of 4 pre-defined points to generate a rectangular ROI. corrects the angle if the 4 points are not rectangular.
        pts = np.float32(
            [[initialcentroidX + 3*initialstddevX, initialcentroidY + 3*initialstddevY], [initialcentroidX + 3*initialstddevX, initialcentroidY - 3*initialstddevY], [initialcentroidX - 3*initialstddevX, initialcentroidY - 3*initialstddevY], [initialcentroidX - 3*initialstddevX, initialcentroidY + 3*initialstddevY]])  # Point set for the printed target test image
        img = transform.perspective_transform(img, pts)
        print("Saving image as ./Data/output_distortion.png.")
        cv2.imwrite('./Data/output_distortion.png', img)

    if gaussian_smooth:
        img = cv2.GaussianBlur(img, (5, 5), 0)
        print("Saving image as ./Data/output_smoothed.png.")
        cv2.imwrite('./Data/output_smoothed.png', img)

    # end of processing, start analysis functions:

    mm_per_pixel = 31/1941  # an approximate conversion factor from pixels to real world distance (in mm) at the standard camera distance. 

    M = cv2.moments(img)
    if M["m00"] != 0:
        centroidX = int(M["m10"] / M["m00"])
        centroidY = int(M["m01"] / M["m00"])
        stddevX = np.sqrt(int(M["mu20"] / M["m00"]))
        stddevY = np.sqrt(int(M["mu02"] / M["m00"]))
    print("Coordinates of centroid (X,Y) (mm): ", mm_per_pixel*(initialcentroidX - 1024), " ", mm_per_pixel*(initialcentroidY - 768))
    print("Std. dev: (X,Y) (mm): ", stddevX*mm_per_pixel, " ", stddevY*mm_per_pixel)

    modified_img = img  # apply filters/overlays to the processed image without losing it

    if map_colours:
        modified_img = cv2.applyColorMap(modified_img, cv2.COLORMAP_JET)
        print("Saving image as ./Data/output_false_colour.png.")
        cv2.imwrite('./Data/output_false_colour.png', modified_img)

    if draw_contours:
        contours, hierarchy = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        modified_image = cv2.drawContours(modified_img, contours, -1, (255, 102, 255), 2)

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
        print("Saving image as ./Data/output_false_colour_centroid.png.")
        cv2.imwrite('./Data/output_false_colour_centroid_std_devs.png', modified_img)

    # end of analysis - begin saving results
 
    csv_exists = os.path.isfile('./Data/' + current_date + '_outputData.csv')  # checks if CSV for today exists.
    with open('./Data/' + current_date + '_outputData.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if csv_exists is False:  # writes in the header if the CSV is new and has no data in it
            writer.writerow(['Time', 'Centroid X(mm)', 'Centroid Y(mm)', 'Std Dev X(mm)', 'Std Dev Y(mm)'])
        writer.writerow([current_time, mm_per_pixel*(initialcentroidX - 1024), mm_per_pixel*(initialcentroidY - 768), stddevX*mm_per_pixel, stddevY*mm_per_pixel])

    end = timer()
    print("Elapsed time:", end - start, "seconds")


if __name__ == "__main__":
    patterns = "*.png"  # checks all files of this type
    ignore_patterns = "*.csv", "*.jpg", "*.tiff", "MandelbrotFractal.png", "MandelbrotFractal.bmp"  # deliberately avoids these filetypes/filenames
    ignore_directories = True  # decides if changes to directories should be ignored as events (leave this True)
    case_sensitive = True
    event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)
    event_handler.on_created = file_made
    # event_handler.on_modified = file_made
    path = "./test_caps"
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)  # recursive determines if subdirectories will be searched
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

