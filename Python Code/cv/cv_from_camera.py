import cv2
import numpy as np
import csv


def nothing(x):
    pass

cap = cv2.VideoCapture(1)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

cv2.namedWindow('canny', cv2.WINDOW_NORMAL)
cv2.resizeWindow('canny', 600, 550)  # Set the desired window size (width, height)
switch = 'OFF / ON'
cv2.createTrackbar(switch, 'canny', 0, 1, nothing)
cv2.createTrackbar('Lower', 'canny',0,255,nothing)
cv2.createTrackbar('Upper', 'canny',0,255,nothing)


while True:

    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image")
        break


    lower = cv2.getTrackbarPos('Lower','canny')
    upper = cv2.getTrackbarPos('Upper', 'canny')
    s = cv2.getTrackbarPos(switch,'canny')


    # Ensure upper >= lower
    if upper < lower:
        upper = lower
        cv2.setTrackbarPos('Upper', 'canny', upper)

    if s == 0:
        edges = frame
    else:
        edges = cv2.Canny(frame, lower, upper)
    
    cv2.imshow('canny',edges)
    key = cv2.waitKey(1) & 0xFF

    if key == 27: # press esc to stop
        break

    if key == 32: # press space to capture image
        coords = np.column_stack(np.where(edges > 0))

        # save edge and original image
        cv2.imwrite('outputs/edges.png', edges)
        cv2.imwrite('outputs/original_img.png',frame)

        # Write coordinates to a CSV file
        csv_filename = 'outputs/raw_edge_coordinates.csv'
        with open(csv_filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            # Write header
            csvwriter.writerow(['X', 'Y'])
            # Write coordinates
            csvwriter.writerows(coords)

        print(f'Edge coordinates saved to {csv_filename}')
        break

cv2.destroyAllWindows()