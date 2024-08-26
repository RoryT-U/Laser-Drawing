import cv2
import numpy as np
import csv
import time
import serial
import pandas as pd
from scipy.spatial import KDTree

def nothing(x):
    pass

cap = cv2.VideoCapture(2)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

cv2.namedWindow('canny', cv2.WINDOW_NORMAL)
cv2.resizeWindow('canny', 500, 500)  # Set the desired window size (width, height)
switch = 'OFF / ON'
cv2.createTrackbar(switch, 'canny', 1, 1, nothing)
cv2.createTrackbar('Lower', 'canny',70,255,nothing)
cv2.createTrackbar('Upper', 'canny',120,255,nothing)

serialPort = serial.Serial(
    port="COM5", baudrate=1500000, bytesize=serial.EIGHTBITS, timeout=0, stopbits=serial.STOPBITS_ONE,parity=serial.PARITY_NONE
)
isPressed = False

IMG = []
MIKE = []

while True:
    key = cv2.waitKey(1) & 0xFF

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


    if True: # press esc to stop
        #cv2.imshow('canny',edges)

        points = np.column_stack(np.where(edges > 0))

        if len(points) < 2:
            continue

        keep_ratio = 3000/len(points)


        # Randomly select a subset of points based on the keep_ratio
        total_points = len(points)
        num_points_to_keep = int(total_points * keep_ratio)
        if num_points_to_keep < 10:  # Ensure at least 2 points are kept
            raise ValueError("keep_ratio is too low, resulting in less than 2 points being kept")
        
        selected_indices = np.random.choice(total_points, num_points_to_keep, replace=True)
        selected_points = points[selected_indices]
        
        # Create a KDTree for finding the nearest neighbors efficiently
        tree = KDTree(selected_points)
        
        # Create a blank image
        max_x = selected_points[:, 0].max() + 10
        max_y = selected_points[:, 1].max() + 10
        image = 255 * np.ones((max_y, max_x, 3), dtype=np.uint8)
        
        # Initialize an array to keep track of visited points
        visited = np.zeros(len(selected_points), dtype=bool)
        
        # Initialize a list to store the path
        path = []

        # Function to find the closest unvisited point
        def find_closest_unvisited_point(current_index):
            distances, indices = tree.query(selected_points[current_index], k=len(selected_points))
            for idx in indices:
                if not visited[idx]:
                    return idx
            return None

        # Start from the first point
        current_index = 0
        visited[current_index] = True
        path.append((selected_points[current_index][0], selected_points[current_index][1]))

        start_point = (selected_points[current_index][0], selected_points[current_index][1])
        
        for _ in range(1, num_points_to_keep):
            next_index = find_closest_unvisited_point(current_index)
            if next_index is None:
                break
            
            end_point = (selected_points[next_index][0], selected_points[next_index][1])
            
            
            # Mark the next point as visited
            visited[next_index] = True
            path.append((selected_points[next_index][0], selected_points[next_index][1]))
            
            # Move to the next point
            start_point = end_point
            current_index = next_index

        path.append((selected_points[0][0], selected_points[0][1]))

        # output = bytearray()
        # for i in range(len(path)):
        #     point = [255-int(path[i][0]//1.9), 255-int(path[i][1]//2.51), 255]
        #     print(point)
        #     output.extend(bytearray(point))

        # output.extend(bytearray([13,13,13]))
        # serialPort.write(output)

        output = []
        for i in range(len(path)):
            point = [255-int(path[i][0]//1.9), 255-int(path[i][1]//2.51), 255]
            #print(point)
            output.extend(point)

        output.extend([13,13,13])
        serialPort.write(bytearray(output))
        #print(bytearray(output))
        print(f"IMG Sent {len(output)} bytes \n\n\n")

        IMG = bytearray(output)


        def readCSV(filename):
            with open(filename, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                row = next(csvreader)

                if row[-1] == '':
                    row = row[:-1]
                int_row = [int(value) for value in row]

                scale = max(int_row) / 255

                scaled_row = [int(value // scale) for value in int_row]

                return scaled_row

        SWAP_XY = False
        FLIP_X = True
        FLIP_Y = True

        def getBytesOfCSV(filename):
            xLst = readCSV(f"Python Code\\Coordinate\\converted_csvs\\{filename}-{'y' if SWAP_XY else 'x'}.csv")
            yLst = readCSV(f"Python Code\\Coordinate\\converted_csvs\\{filename}-{'x' if SWAP_XY else 'y'}.csv")

            xLst = [255-val for val in xLst] if FLIP_X else xLst
            yLst = [255-val for val in yLst] if FLIP_Y else yLst

            output = []
            for i in range(len(xLst)):
                output.extend([xLst[i], yLst[i], 255])

            return bytearray(output + [13,13,13])


            #### READ DATA
        output = getBytesOfCSV("mike-300")
        #serialPort.write((output))
        # print(output)
        # MIKE = output
        # print(f"MIKE sent {len(output)} bytes")

        #time.sleep(0.1)


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

print(list(IMG))
print(list(MIKE))

cv2.destroyAllWindows()