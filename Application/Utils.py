# pip install pyserial

import csv
import math
import numpy as np
SWAP_XY = False
FLIP_X = True
FLIP_Y = True


class CSVReader:
    def __init__(self):
        pass


    ''' Reads a single CSV file with a single axis of values (e.g. a list of X-values)
    '''
    @staticmethod
    def _readAxisCSV(filename):
        with open(filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            row = next(csvreader)

            if row[-1] == "":
                row = row[:-1]
            int_row = [int(value) for value in row]

            scale = max(int_row) / 255

            scaled_row = [int(value // scale) for value in int_row]

            return scaled_row

    ''' Combines seperate axis CSVs denoted by {filename}-x and {filename}-y into a drawable
        data stream. Draws a single line; laser does not turn off.
    '''
    @staticmethod
    def getBytesOfAxisCSV(filename):
        xLst = CSVReader._readAxisCSV(
            f"Python Code\\Coordinate\\converted_csvs\\{filename}-{'y' if SWAP_XY else 'x'}.csv"
        )
        yLst = CSVReader._readAxisCSV(
            f"Python Code\\Coordinate\\converted_csvs\\{filename}-{'x' if SWAP_XY else 'y'}.csv"
        )

        xLst = [255 - val for val in xLst] if FLIP_X else xLst
        yLst = [255 - val for val in yLst] if FLIP_Y else yLst

        output = []
        for i in range(len(xLst)):
            output.extend([xLst[i], yLst[i], 48])

        return output


class Shapes:
    def __init__(self):
        pass

    @staticmethod
    def broken_cirle():
        POINTS = 2040
        RES = 255
        arr = []

        for i in range(POINTS):
            x = RES * math.sin(2 * math.pi * i / POINTS) + RES / 2
            y = RES * math.cos(2 * math.pi * i / POINTS) + RES / 2
            arr.extend([int(math.floor(x)), int(math.floor(y)), 0 if i % 2 else 255])
        return arr

    @staticmethod
    def circle():
        POINTS = 360
        GAP = 5

        x = np.linspace(0, POINTS, POINTS)
        sine = np.round(127 * np.sin((2 * np.pi * x) / POINTS) + 128)
        cos = np.round(127 * np.cos((2 * np.pi * x) / POINTS) + 128)

        arr = []
        for i in range(POINTS):

            arr.extend(
                [
                    int(sine[i]),
                    int(cos[i]),
                    0 if i % GAP * 2 > GAP and cos[i] < 128 else 255,
                ]
            )

        print(arr)
        return arr

    @staticmethod
    def square():
        POINTS = 255

        arr = []
        for i in range(POINTS):
            arr.extend([i, 0, 255])
        arr.extend([255, 0, 255])
        for i in range(POINTS):
            arr.extend([255, i, 255])
        arr.extend([255, 255, 255])
        for i in range(POINTS):
            arr.extend([255 - i, 255, 255])
        arr.extend([0, 255, 255])
        for i in range(POINTS):
            arr.extend([0, 255 - i, 255])
        arr.extend([0, 0, 255])

        print(arr + [13,13,13])
        return arr + [13,13,13]

    @staticmethod
    def lines():
        points = 255

        delay_start = 0
        delay_end = 20
        arr = []

        for i in range(0, points, 5):
            arr.extend([i, 0, 255])
        arr[-1] = 0
        # arr.extend([255, 0, 0])
        for _ in range(delay_start):
            arr.extend([255, 0, 0])

        for _ in range(delay_end):
            arr.extend([0, 255, 0])

        for i in range(0, points, 5):
            arr.extend([i, 255, 255])

        arr[-1] = 0

        for _ in range(delay_start):
            arr.extend([255, 255, 0])

        for _ in range(delay_end):
            arr.extend([0, 0, 0])
            
        print(arr)
        return arr


    @staticmethod
    def rectangle_points(x:int, y:int, width:int, height:int, corner_len:int, corner_repeats:int, num_non_corner_points:int):
        points = []
        corner_points = (corner_len * 2 - 1) * corner_repeats
        width_without_corners = width - 2 * corner_len + 1
        height_without_corners = height - 2 * corner_len + 1

        width_height_ratio = width_without_corners/height_without_corners

        num_points_on_width = round((num_non_corner_points) * width_height_ratio / 2)
        num_points_on_height = round((num_non_corner_points - num_points_on_width*2) / 2)
        print(corner_points, num_points_on_width, num_points_on_height)

        try: 
            gap_between_width_points = width_without_corners/num_points_on_width
            gap_between_height_points = height_without_corners/num_points_on_height
        except Exception:
            gap_between_width_points = 0
            gap_between_height_points = 0

        print(gap_between_width_points, gap_between_height_points)

        # Top left Corner
        for i in range(0, corner_len):
            for _ in range(0, corner_repeats):
                points.append([x+i, y])

        
        # Add Top Side 
        for i in range(1, num_points_on_width):
            points.append([x + corner_len - 1 + (i)*gap_between_width_points, y])

        # Top Right Corner
        for i in range(width-corner_len, width):
            for _ in range(0, corner_repeats):
                points.append([x+i,y])
        
        for j in range(1, corner_len):
            for _ in range(0, corner_repeats):
                points.append([x+width-1,y+j])
        
        # Add Right Side
        for j in range(1, num_points_on_height):
            points.append([x+width-1, y+corner_len - 1 + j*gap_between_height_points])

        # Bottom Right Corner
        for j in range(height-corner_len, height):
            for _ in range(0, corner_repeats):
                points.append([x+width-1,y+j])
        
        for i in range(width-2, width-corner_len-1, -1):
            for _ in range(0, corner_repeats):
                points.append([x+i,y+height-1])

        # Add Bottom Side 
        for i in range(num_points_on_width-1, 0, -1):
            points.append([x + corner_len - 1 + (i)*gap_between_width_points, y+height-1])

        # Bottom Left Corner
        for i in range(corner_len-1, -1, -1):
            for _ in range(0, corner_repeats):
                points.append([x+i,y+height-1])

        for j in range(1, corner_len):
            for _ in range(0, corner_repeats):
                points.append([x,y+height-1-j])

        # Add Right Side
        for i in range(1, num_points_on_height):
            points.append([x, y+height - corner_len - i*gap_between_height_points])

        # Close Top Left Corner
        for j in range(corner_len-1, 0, -1):
            for _ in range(0, corner_repeats):
                points.append([x, y+j])

        points.append(points[0])

        print(len(points))
        print(points)

        return points