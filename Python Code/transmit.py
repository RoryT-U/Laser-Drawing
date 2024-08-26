import time
import random
import csv
import PSoCBridge

PSoCBridge.Initialise("COM5")

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
DATA = getBytesOfCSV("mike-1000")

#DATA = bytearray([random.choice(range(255)) for _ in range(997)] + [13,13,13])

def dataTest():
    FRAMES = 50
    # send frames
    start = time.perf_counter()
    for i in range(0,FRAMES):
        serialPort.write(DATA)
    serialPort.write(bytearray([13,13,13,13]))

    # wait for ACK
    while 1:
        serialString = serialPort.readline()
        if serialString:
            print(serialString.decode("ascii"))
            break

    stop = time.perf_counter()
    elapsed = stop - start
    numBytes = FRAMES*len(DATA)
    print(f"recieved {FRAMES} frames ({numBytes} bytes) in {elapsed:0.4f} seconds ({numBytes*8/elapsed/1000:0.0f} Kbps)")


def transmit(filename):
    transmitting = getBytesOfCSV(filename)
    serialPort.write(transmitting)
    print(f"sent {len(transmitting)} bytes")
    time.sleep(3)

while 1:
    userInput = input()

    if (userInput == "data"):
        sendData()
    elif (userInput == "speed"):
        dataTest()

    elif (userInput == "test"):
        transmit("atom-500")
        transmit("atom-1000")
        transmit("circle-510")
        transmit("circle-2040")
        transmit("image-4000")
        transmit("image-1500")
        transmit("mike-750")
        transmit("mike-1000")


    elif (userInput == "pause"):
        serialPort.write(bytearray([0,13,13,13]))
    elif (userInput[:5] == "send "):
        print(userInput[5:])
        transmit(userInput[5:])
    else:
        serialPort.write(str.encode(userInput, "ascii"))



