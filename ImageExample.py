import cv2
import numpy as np
import epics
import transform
from timeit import default_timer as timer

start = timer()

img1 = cv2.imread('laserspoton.png', 0)
img2 = cv2.imread('laserspotoff.png', 0)


diffed_img = transform.brightness_difference(img1, img2)
print("Saving image as subtraction_output.png.")
cv2.imwrite('output_subtraction.png', diffed_img)


#pts = np.float32([[1849, 912], [2845, 882], [2889, 1880], [1887, 1918]]) #Point set for the printed target test image
pts = np.float32([[901, 803], [2217, 807], [747, 1393], [2385, 1393]]) #Point set for the Dental Clinic business card test image
warped = transform.perspective_transform(diffed_img, pts)
print("Saving image as distortion_output.png.")
cv2.imwrite('output_distortion.png', warped)


false_colour = cv2.applyColorMap(diffed_img, cv2.COLORMAP_JET)
print("Saving image as false_colour_output.png.")
cv2.imwrite('output_false_colour.png', false_colour)


M = cv2.moments(diffed_img)
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
print("Coordinates of centroid (X,Y): ", cX, " ", cY)
false_colour_centroid = cv2.circle(false_colour, (cX, cY), 20, (255, 102, 255), 3)
print("Saving image as output_false_colour_centroid.png.")
cv2.imwrite('output_false_colour_centroid.png', false_colour_centroid)


end = timer()
print("Elapsed time:", end - start,"seconds")