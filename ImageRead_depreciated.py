import cv2
import numpy as np

img1 = cv2.imread('card_flash.jpg', 0)
img2 = cv2.imread('card_no_flash.jpg', 0)

result_img = cv2.absdiff(img1, img2)

print("Saving image as subtraction_output.png.")
cv2.imwrite('subtraction_output.png', result_img)

rect = np.zeros((4, 2), dtype="float32")

pts = np.float32([[901, 803],[2217, 807],[747, 1393],[2385, 1393]])

s = pts.sum(axis=1)
rect[0] = pts[np.argmin(s)]
rect[2] = pts[np.argmax(s)]

diff = np.diff(pts, axis=1)
rect[1] = pts[np.argmin(diff)]
rect[3] = pts[np.argmax(diff)]
(tl, tr, br, bl) = rect

widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
maxWidth = max(int(widthA), int(widthB))

heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
maxHeight = max(int(heightA), int(heightB))

dst = np.array([
    [0, 0],
    [maxWidth - 1, 0],
    [maxWidth - 1, maxHeight - 1],
    [0, maxHeight - 1]], dtype="float32")

M = cv2.getPerspectiveTransform(rect,dst)
image = cv2.warpPerspective(img2, M, (maxWidth, maxHeight))

cv2.imshow('image', result_img)
k = cv2.waitKey(0)

print("Saving image as distortion_output.png.")
cv2.imwrite('distortion_output.png', result_img)
