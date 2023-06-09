import cv2 as cv
import numpy as np
import keyboard
from matplotlib import pyplot as plt


r"""img1 = cv.imread(r'C:\Users\damwid001\PycharmProjects\Astropi2022-2023\Data\Image1.jpg', 1)
img1 = cv.resize(img1,(410,308))
img2 = cv.imread(r'C:\Users\damwid001\PycharmProjects\Astropi2022-2023\Data\Image2.jpg', 1)
img2 = cv.resize(img2,(410,308))"""

x_offset = 0
y_offset = 0
p1 = 0,0
p2 = 0,0
imglast = None

sift = cv.SIFT_create()
# find the keypoints and descriptors with SIFT


for x in range(4):
    number = 62 - x

    img = cv.imread(r'C:\Users\damwid001\PycharmProjects\Astropi2022-2023\Data\Image'+ str(number) +'.jpg', 1)
    img = cv.resize(img, (410, 308)) #(410, 308)

    if imglast is not None:

        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        imglast_gray = cv.cvtColor(imglast, cv.COLOR_BGR2GRAY)
        kp1, des1 = sift.detectAndCompute(img_gray, None)
        kp2, des2 = sift.detectAndCompute(imglast_gray, None)
        FLANN_INDEX_KDTREE = 1
        index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        search_params = dict(checks=50)
        flann = cv.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)
        num = 0
        while True:
            p1 = kp1[good[num].queryIdx].pt
            p2 = kp2[good[num].trainIdx].pt

            x_offset_in = int(x_offset + p2[0])
            y_offset_in = int(y_offset + p2[1])
            x_end_in = x_offset_in + img.shape[1]
            y_end_in = y_offset_in + img.shape[0]

            print(p1, "space", p2, "Num", num, y_offset, y_offset_in)

            imgb = np.zeros((y_end_in, x_end_in, 3), dtype=np.uint8)
            imgb[0:y_end_last, 0:x_end_last] = imgb1
            imgb[y_offset_in:y_end_in, x_offset_in:x_end_in] = img

            cv.imshow('image', imgb)
            cv.waitKey(0)

            #while not keyboard.is_pressed("y"):
            #    pass

            if keyboard.is_pressed("q"):
                x_end = x_end_in
                y_end = y_end_in
                y_offset = y_offset_in
                x_offset = x_offset_in
                break
            num += 1


    if imglast is None:

        x_end = x_offset + img.shape[1]
        y_end = y_offset + img.shape[0]
        imgb = np.zeros((y_end, x_end, 3), dtype = np.uint8)
        imgb[0:y_end, 0:x_end] = img


    x_end_last = x_end
    y_end_last = y_end

    print(x_offset)

    imgb1 = imgb
    imglast = img



    #imgb[0:308,0:410] = img2
#print(type(img1.dtype))
#img = cv2.addWeighted(img1, 0.3, img2, 0.7, 0)


cv.imshow('image', imgb)

cv.waitKey(0)
print("end")


"""if len(good) > 4:
    src_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
    M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
    matchesMask = mask.ravel().tolist()
    h, w = img_gray.shape
    pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1], [w - 1, 0]]).reshape(-1, 1, 2)
    dst = cv.perspectiveTransform(pts, M)
    out_imglast_gray = cv.polylines(imglast_gray, [np.int32(dst)], True, 255, 3, cv.LINE_AA)

    draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                       singlePointColor=None,
                       matchesMask=matchesMask,  # draw only inliers
                       flags=2)
    # print(dst)
    img3 = cv.drawMatches(img, kp1, out_imglast_gray, kp2, good, None, **draw_params)
    plt.imshow(img3, 'gray'), plt.show()

else:
    print("Not enough matches are found - {}/{}".format(len(good), 4))
    matchesMask = None"""