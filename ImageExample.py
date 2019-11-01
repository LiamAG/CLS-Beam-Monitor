import cv2
import numpy as np
import transform
from timeit import default_timer as timer

start = timer()

img1 = cv2.imread('card_flash.jpg', 0)
img2 = cv2.imread('card_no_flash.jpg', 0)

diffed_img = transform.brightness_difference(img1, img2)

print("Saving image as subtraction_output.png.")
cv2.imwrite('output_subtraction.png', diffed_img)

#pts = np.float32([[1849, 912], [2845, 882], [2889, 1880], [1887, 1918]]) #Point set for the printed target test image
pts = np.float32([[901, 803], [2217, 807], [747, 1393], [2385, 1393]]) #Point set for the Dental Clinic business card test image


warped = transform.perspective_transform(diffed_img, pts)

print("Saving image as distortion_output.png.")
cv2.imwrite('output_distortion.png', warped)

end = timer()

print("Elapsed time:", end - start,"seconds")
