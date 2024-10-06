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
            output.extend([xLst[i], yLst[i], 255])

        return output + [13,13,13]


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
            if x > 255 or y > 255:
                print(x, y, "shit")
            arr.extend([int(math.floor(x)), int(math.floor(y)), 0 if i % 2 else 255])
        arr.extend([13, 13, 13])
        return arr

    @staticmethod
    def circle():
        POINTS = 360
        GAP = 5

        x = np.linspace(0, POINTS, POINTS)
        sine = np.round(127 * np.sin((2 * np.pi * x) / POINTS) + 128)
        cos = np.round(127 * np.cos((2 * np.pi * x) / POINTS) + 128)

        arr = []
        count = 0
        for i in range(POINTS):

            arr.extend(
                [
                    int(sine[i]),
                    int(cos[i]),
                    0 if i % GAP * 2 > GAP and cos[i] < 128 else 255,
                ]
            )

        arr.extend([13, 13, 13])

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

        arr.extend([13, 13, 13])

        print(arr)
        return arr

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

        arr.extend([13, 13, 13])
        print(arr)
        return arr
