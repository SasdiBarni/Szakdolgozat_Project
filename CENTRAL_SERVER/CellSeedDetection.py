import cv2
import numpy as np

def CellSeedDetectAndCount(tile):

    img = np.array(tile)
    blur = cv2.medianBlur(img, 5)
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)

    thresh_for_seeds = cv2.threshold(gray, 135, 255, cv2.THRESH_TOZERO_INV)[1]

    cnts_for_seeds = cv2.findContours(thresh_for_seeds, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    cnts_for_seeds = cnts_for_seeds[0] if len(cnts_for_seeds) == 2 else cnts_for_seeds[1]

    min_area = 1
    black_dots = []

    for c in cnts_for_seeds:
        area = cv2.contourArea(c)
        if area > min_area:
            cv2.drawContours(img, [c], -1, (36, 255, 12), 1)
            black_dots.append(c)
            
    return black_dots