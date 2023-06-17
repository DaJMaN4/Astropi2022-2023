import cv2 as cv
import numpy as np
import keyboard


img = cv.imread("Work-Photos" + input("Name of photo in Work-Photos") + ".png", 1)


kernel = np.ones((5,5),np.uint8)
img1 = cv.GaussianBlur(img, (7, 7), 0)
img2 = cv.Canny(img1, 100, 100)
img3 = cv.dilate(img2, kernel, iterations=1)
img4 = cv.erode(img3, kernel, iterations=1)

# Make a True/False mask of pixels whose BGR values sum to more than zero
alpha = np.sum(img, axis=-1) > 0

# Convert True/False to 0/255 and change type to "uint8" to match "na"
alpha = np.uint8(alpha * 255)

# Stack new alpha layer with existing image to go from BGR to BGRA, i.e. 3 channels to 4 channels
res = np.dstack((img, alpha))

# Save result
cv.imshow('result.png', res)
cv.imshow('img', img)
cv.imshow('img1', img1)

cv.waitKey(0)

