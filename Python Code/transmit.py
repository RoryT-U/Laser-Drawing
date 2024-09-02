import math
import time
import csv

import PSoCBridge

# connect to COM port and PSoC
PSoC = PSoCBridge.PSoCBridge()

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
        color = 255
        # if i > 0 and (abs(xLst[i]-xLst[i-1]) + abs(yLst[i]-yLst[i-1])) > 25:    # Euclidean (faster??)
        if i > 0 and math.sqrt(math.pow(xLst[i]-xLst[i-1], 2) + math.pow(yLst[i]-yLst[i-1],2)) > 25:
            color = 0
        output.extend([xLst[i], yLst[i], color])

    return bytearray(output)

def transmit(filename):
    PSoC.write(getBytesOfCSV(filename))
    time.sleep(3)

while 1:
    userInput = input()

    if (userInput == "speed"):
        PSoC.speed_test()

    elif (userInput == "test"):
        transmit("atom-500")
        transmit("atom-1000")
        transmit("circle-510")
        transmit("circle-2040")
        transmit("image-4000")
        transmit("image-1500")
        transmit("mike-750")
        transmit("mike-1000")

    # turn laser ON/OFF
    elif (userInput == "ON"):
        PSoC.write([255,255,255])
    elif (userInput == "OFF"):
        PSoC.write([0,0,0])
    elif (userInput[:5] == "send "):
        print(userInput[5:])
        transmit(userInput[5:])
    else:
        PSoC.write_unterminated(str.encode(userInput, "ascii"))



