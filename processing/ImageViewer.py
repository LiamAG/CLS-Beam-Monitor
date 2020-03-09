import cv2 
import numpy as np
import transform


img_original = cv2.imread("./Data/original_image.png")
img_subtract = cv2.imread("./Data/output_subtraction.png")
img_false = cv2.imread("./Data/output_false_colour.png")
img_cent_devs = cv2.imread("./Data/output_false_colour_centroid_std_devs.png")

while 1:
    original_and_subtract = np.concatenate((img_original, img_subtract), axis=1)
    cv2.imshow("Original and Background Subtraction Images", original_and_subtract)
    cv2.waitKey(100)

cv2.destroyAllWindows()