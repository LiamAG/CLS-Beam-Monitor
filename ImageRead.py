import cv2
import numpy as np

img1 = cv2.imread('flash_angular_distortion.jpg', 0)
img2 = cv2.imread('no_flash_angular_distortion.jpg', 0)


result_img = cv2.absdiff(img1, img2)

cv2.imshow('image', result_img)
k = cv2.waitKey(0)

if k == ord('s'):
    print("Saving image as subtraction_output.png.")
    cv2.imwrite('subtraction_output.png', result_img)
else:
    cv2.destroyAllWindows()

pts1 = np.float32([[1885, 1921], [1849, 909], [2893, 1881], [2853, 885]])
pts2 = np.float32([[0, 0], [800, 0], [0, 800], [800, 800]])

M = cv2.getPerspectiveTransform(pts1,pts2)

result_img = cv2.warpPerspective(result_img,M,(800,800))

print(result_img)

cv2.imshow('image', result_img)
k = cv2.waitKey(0)

if k == ord('s'):
    print("Saving image as distortion_output.png.")
    cv2.imwrite('distortion_output.png', result_img)
else:
    cv2.destroyAllWindows()