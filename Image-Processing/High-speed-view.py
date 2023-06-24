import cv2 as cv
import numpy as np

imgstart = cv.imread("Work-Photos\\" + input("Name of photo in Work-Photos") + ".png", 1)
img = imgstart
kernel = np.ones((5,5),np.uint8)

for x in range(3):
    img = cv.blur(img, (3, 20))

image2 = cv.dilate(img, kernel, iterations=1)
img2 = cv.Canny(img, 100, 100)

alpha = np.sum(img, axis=-1) > 0
alpha = np.uint8(alpha * 255)
res = np.dstack((img, alpha))

sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])

sharpen = cv.filter2D(img, -1, sharpen_kernel)
sharpen2 = cv.filter2D(sharpen, -1, sharpen_kernel)
res = cv.blur(sharpen2, (4, 4))

cv.imshow('result.png', res)
cv.imshow('img', imgstart)
cv.waitKey(0)

