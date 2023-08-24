import cv2
import numpy as np
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
from numpy.lib.polynomial import poly

img = cv2.imread('C:\\Users\\sasdi\\Documents\\Szakdolgozat_Other\\Sample_1.bmp')
blur = cv2.medianBlur(img, 5)
gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

thresh_for_black_dots = cv2.threshold(gray,100,255, cv2.THRESH_BINARY_INV)[1]

cnts_for_black_dots = cv2.findContours(thresh_for_black_dots, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cnts_for_black_dots = cnts_for_black_dots[0] if len(cnts_for_black_dots) == 2 else cnts_for_black_dots[1]

min_area = 1
black_dots = []
        
for c in cnts_for_black_dots:
   area = cv2.contourArea(c)
   if area > min_area:
      cv2.drawContours(img, [c], -1, (36, 255, 12), 1)
      black_dots.append(c)

print("Cell Seed Count is:",len(black_dots))

cv2.imshow('Output image:', img)
cv2.waitKey()

'''
im = cv2.imread('C:\\Users\\sasdi\\Documents\\Szakdolgozat_Other\\Sample_4.bmp')
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()
 
# Detect blobs.
keypoints = detector.detect(gray)
print("Cellseed Count is:",len(keypoints))

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0,255,0), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
 
# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
'''

'''
img = cv2.imread('C:\\Users\\sasdi\\Documents\\Szakdolgozat_Other\\Sample_4.bmp')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)


#cv2.imshow('Binary image', thresh)
#cv2.imshow('image_thres1.jpg', thresh)
#cv2.waitKey(0)

contours, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

image_copy = img.copy()
cv2.drawContours(image=image_copy, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)
                
# see the results
cv2.imshow('None approximation', image_copy)
cv2.imshow('contours_none_image1.jpg', image_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
print(len(contours))


# filter by area
s1 = 3
s2 = 20
xcnts = []
for cnt in contours:
    if s1<cv2.contourArea(cnt) <s2:
        xcnts.append(cnt)
        
print("\nDots number: {}".format(len(xcnts)))
'''