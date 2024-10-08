import cv2
import numpy as np
import csv
from scipy.spatial import KDTree
from cvzone.SelfiSegmentationModule import SelfiSegmentation
from PSoCBridge import PSoCBridge


class CV:
    segmentor = SelfiSegmentation()
    running = True
    show_preview = 0

    def __init__(self, PSoC: PSoCBridge, camera: int) -> None:
        self.camera = camera
        self.PSoC = PSoC
        self.cap = cv2.VideoCapture(camera)
        self.lower = 50
        self.upper = 70
        print(f"running CV with camera {camera}")

    @staticmethod
    def nothing(x):
        pass

    def camera_preview(self, show_preview):
        self.show_preview = show_preview

    def stop(self):
        self.running = False

    def runCV(self):
        if not self.cap.isOpened():
            raise FileNotFoundError("Camera not found! Change the selected camera!")

        while self.running:
            key = cv2.waitKey(1) & 0xFF

            ret, frame = self.cap.read()
            frame = cv2.resize(frame, (255, 255))

            if not ret:
                print("Error: Failed to capture image")
                break

            lower = 55
            upper = 55
            s = 1
            BG_threshold = 800 / 1000  # cv2.getTrackbarPos('BG Threshold', 'canny')

            frame = self.segmentor.removeBG(
                frame, (0, 255, 0), cutThreshold=BG_threshold
            )

            if s == 0:
                edges = frame
            else:
                edges = cv2.Canny(frame, lower, upper)

            ###### Previewing the image!
            if self.show_preview == 0:
                cv2.destroyAllWindows()
            elif self.show_preview == 1:
                cv2.imshow('Computer Vision Preview',edges)
            elif self.show_preview == 2:
                cv2.imshow('Computer Vision Preview',frame)

            if True:  # press esc to stop
                # cv2.imshow('canny',edges)

                points = np.column_stack(np.where(edges > 0))

                if len(points) < 2:
                    continue

                keep_ratio = 1000 / len(points)

                # Randomly select a subset of points based on the keep_ratio
                total_points = len(points)
                num_points_to_keep = int(total_points * keep_ratio)
                if num_points_to_keep < 10:  # Ensure at least 2 points are kept
                    print(
                        "keep_ratio is too low, resulting in less than 2 points being kept"
                    )

                selected_indices = np.random.choice(
                    total_points, num_points_to_keep, replace=True
                )
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
                    distances, indices = tree.query(
                        selected_points[current_index], k=len(selected_points)
                    )
                    for i in range(len(indices)):
                        if not visited[indices[i]]:
                            return indices[i], distances[i]
                    return None, 0

                # Start from the first point
                current_index = 0
                visited[current_index] = True
                path.append(
                    (
                        selected_points[current_index][0],
                        selected_points[current_index][1],
                        0,
                    )
                )

                start_point = (
                    selected_points[current_index][0],
                    selected_points[current_index][1],
                )

                for _ in range(1, num_points_to_keep):
                    next_index, dist = find_closest_unvisited_point(current_index)
                    if next_index is None:
                        break

                    end_point = (
                        selected_points[next_index][0],
                        selected_points[next_index][1],
                    )

                    # Mark the next point as visited
                    visited[next_index] = True
                    LED = 255
                    if dist > 10:
                        LED = 0
                        for _ in range(2):
                            path.append(
                                (
                                    selected_points[next_index][0],
                                    selected_points[next_index][1],
                                    LED,
                                )
                            )
                    path.append(
                        (
                            selected_points[next_index][0],
                            selected_points[next_index][1],
                            LED,
                        )
                    )

                    # Move to the next point
                    start_point = end_point
                    current_index = next_index

                # path.append((selected_points[0][0], selected_points[0][1], 255))

                # output = bytearray()
                # for i in range(len(path)):
                #     point = [255-int(path[i][0]//1.9), 255-int(path[i][1]//2.51), 255]
                #     print(point)
                #     output.extend(bytearray(point))

                # serialPort.write(output)

                output = []
                swap = True
                for i in range(len(path)):
                    X = 255 - int(path[i][0] // 1.9)
                    Y = 255 - int(path[i][1] // 2.51)
                    if swap:
                        X = 255 - int(path[i][1])
                        Y = 255 - int(path[i][0])

                    point = [X, Y, int(path[i][2])]
                    # print(point)
                    output.extend(point)

                self.PSoC.write(output)
                # print(bytearray(output))

                IMG = bytearray(output)

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

        print("stopped CV")

        cv2.destroyAllWindows()
