import cv2
import numpy as np
import epics
import transform
from timeit import default_timer as timer
from epics import PV

start = timer()

img1 = cv2.imread('laser1.png', 0)
img2 = cv2.imread('backround.png', 0)

diffed_img = transform.brightness_difference(img1, img2)
print("Saving image as output_subtraction.png.")
cv2.imwrite('output_subtraction.png', diffed_img)

#pts = np.float32([[1849, 912], [2845, 882], [2889, 1880], [1887, 1918]]) #Point set for the printed target test image
#pts = np.float32([[901, 803], [2217, 807], [747, 1393], [2385, 1393]]) #Point set for the Dental Clinic business card test image
#warped = transform.perspective_transform(diffed_img, pts)
#print("Saving image as distortion_output.png.")
#cv2.imwrite('output_distortion.png', warped)

diffed_img = cv2.GaussianBlur(diffed_img, (5,5), 0)

false_colour = cv2.applyColorMap(diffed_img, cv2.COLORMAP_JET)
print("Saving image as output_false_colour.png.")
cv2.imwrite('output_false_colour.png', false_colour)

M = cv2.moments(diffed_img)
centroidX = int(M["m10"] / M["m00"])
centroidY = int(M["m01"] / M["m00"])
stddevX = np.sqrt(int(M["mu20"] / M["m00"]))
stddevY = np.sqrt(int(M["mu02"] / M["m00"]))
print("Coordinates of centroid (X,Y): ", centroidX, " ", centroidY)
print("Std. dev: (X,Y): ", stddevX, " ", stddevY)

false_colour_centroid = cv2.circle(false_colour, (centroidX, centroidY), 20, (255, 102, 255), 3) #plots the centroid as a circle

false_colour_centroid = cv2.line(false_colour_centroid, (centroidX + int(stddevX), centroidY + 30), (centroidX + int(stddevX), centroidY - 30), (255, 102, 255), 3) #plots the first standard deviation from the centroid in x and y
false_colour_centroid = cv2.line(false_colour_centroid, (centroidX - int(stddevX), centroidY + 30), (centroidX - int(stddevX), centroidY - 30), (255, 102, 255), 3)
false_colour_centroid = cv2.line(false_colour_centroid, (centroidX + 30, centroidY + int(stddevY)), (centroidX - 30, centroidY + int(stddevY)), (255, 102, 255), 3)
false_colour_centroid = cv2.line(false_colour_centroid, (centroidX + 30, centroidY - int(stddevY)), (centroidX - 30, centroidY - int(stddevY)), (255, 102, 255), 3)

false_colour_centroid = cv2.line(false_colour_centroid, (centroidX + 2*int(stddevX), centroidY + 30), (centroidX + 2*int(stddevX), centroidY - 30), (255, 102, 255), 3) #plots the second standard deviation from the centroid in x and y
false_colour_centroid = cv2.line(false_colour_centroid, (centroidX - 2*int(stddevX), centroidY + 30), (centroidX - 2*int(stddevX), centroidY - 30), (255, 102, 255), 3)
false_colour_centroid = cv2.line(false_colour_centroid, (centroidX + 30, centroidY + 2*int(stddevY)), (centroidX - 30, centroidY + 2*int(stddevY)), (255, 102, 255), 3)
false_colour_centroid = cv2.line(false_colour_centroid, (centroidX + 30, centroidY - 2*int(stddevY)), (centroidX - 30, centroidY - 2*int(stddevY)), (255, 102, 255), 3)

print("Saving image as output_false_colour_centroid.png.")
cv2.imwrite('output_false_colour_centroid.png', false_colour_centroid)

end = timer()
print("Elapsed time:", end - start,"seconds")

