import cv2      # `python -m pip install -U opencv-python`
import matplotlib.pyplot as plt
import cvzone   # `python -m pip install -U cvzone` and `python -m pip install -U mediapipe
from cvzone.SelfiSegmentationModule import SelfiSegmentation
import numpy as np
import csv

segmentor = SelfiSegmentation()

def nothing(x):
    pass

filename = "kev"

img = cv2.imread(f'Python Code\\cv\\{filename}.png')

assert img is not None

img = cv2.resize(img, (400,400))

cv2.namedWindow('canny')
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'canny', 0, 1, nothing)
cv2.createTrackbar('Lower', 'canny',0,255,nothing)
cv2.createTrackbar('Upper', 'canny',0,255,nothing)
cv2.createTrackbar('Remove BG', 'canny',0,1,nothing)
cv2.createTrackbar('BG Threshold', 'canny',0,1000,nothing)


while True:
    lower = cv2.getTrackbarPos('Lower','canny')
    upper = cv2.getTrackbarPos('Upper', 'canny')
    BG = cv2.getTrackbarPos('Remove BG', 'canny')
    BG_threshold = cv2.getTrackbarPos('BG Threshold', 'canny')
    s = cv2.getTrackbarPos(switch,'canny')

    res = img
    # remove bg - doesnt really help yet, e.g. cuts thumb, needs cleaner bg?
    if BG:
        res = segmentor.removeBG(img, (0,255,0) ,cutThreshold=BG_threshold/1000)

    # Ensure upper >= lower
    if upper < lower:
        upper = lower
        cv2.setTrackbarPos('Upper', 'canny', upper)

    if s == 0:
        edges = res
    else:
        edges = cv2.Canny(res, lower, upper)
    
    cv2.imshow('canny',edges)
    key = cv2.waitKey(1) & 0xFF

    if key == 27: # press esc to stop
        break

    if key == 32: # press space to capture image
        coords = np.column_stack(np.where(edges > 0))

        # save edge image
        cv2.imwrite(f'Python Code\\cv\\out\\{filename}-e.png', edges)

        # Write coordinates to a CSV file
        # TODO: Why doesnt this workkkkk
        csv_filename = f'Python Code\\cv\\out\\{filename}.csv'
        with open(csv_filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write header
            csvwriter.writerow(['X', 'Y'])
            # Write coordinates
            csvwriter.writerows(coords)

        print(f'Edge coordinates saved to {csv_filename}')
        break

cv2.destroyAllWindows()
