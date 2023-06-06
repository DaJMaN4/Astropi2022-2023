import cv2
import numpy as np


img1 = cv2.imread(r'C:\Users\damwid001\PycharmProjects\Astropi2022-2023\Data\Image1.jpg', 1)
img1 = cv2.resize(img1,(410,308))
img2 = cv2.imread(r'C:\Users\damwid001\PycharmProjects\Astropi2022-2023\Data\Image2.jpg', 1)
img2 = cv2.resize(img2,(410,308))

x_offset = 0
y_offset = 0


for x in range(4):
    number = 20 - x

    img = cv2.imread(r'C:\Users\damwid001\PycharmProjects\Astropi2022-2023\Data\Image'+ str(number) +'.jpg', 1)
    img = cv2.resize(img, (200, 158)) #(410, 308)

    x_end = x_offset + img.shape[1]
    y_end = y_offset + img.shape[0]

    if x == 0:
        imgb = np.zeros((y_end, x_end, 3), dtype = np.uint8)
        imgb[0:y_end, 0:x_end] = img

    else:
        imgb = np.zeros((y_end, x_end, 3), dtype=np.uint8)
        imgb[0:y_end_last, 0:x_end_last] = imgb1
        imgb[y_offset:y_end, x_offset:x_end] = img

    x_end_last = x_end
    y_end_last = y_end

    x_offset = x_end
    y_offset = y_end

    imgb1 = imgb



    #imgb[0:308,0:410] = img2
#print(type(img1.dtype))
#img = cv2.addWeighted(img1, 0.3, img2, 0.7, 0)


cv2.imshow('image', imgb)

cv2.waitKey(0)

