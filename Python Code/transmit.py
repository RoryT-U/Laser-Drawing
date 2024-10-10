# pip install pyserial

# note we only support 8 bits at the moment!

import serial
import time
from threading import Thread
import random
import csv
import math
import numpy as np

colour = 255

serialPort = serial.Serial(
    port="COM7", baudrate=1500000, bytesize=serial.EIGHTBITS, timeout=0, stopbits=serial.STOPBITS_ONE,parity=serial.PARITY_NONE
)

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
        output.extend([xLst[i], yLst[i], i % 255])

    return bytearray(output + [13,13,13])



DATA = bytearray([random.choice(range(255)) for _ in range(997)] + [13,13,13])


def readSerial():
    successes = 0
    while 1:
    # Read data out of the buffer until a carraige return / new line is found
        #serialString = serialPort.read_until(expected="\n", size=10)

        serialString = serialPort.readline()
        if serialString:
            try:
                print(serialString.decode("ascii"))
            except:
                print(serialString)


readThread = Thread(target = readSerial)
readThread.daemon = True
readThread.start()


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


def sendData():
    serialPort.write(DATA)
    print(f"sent {len(DATA)} bytes")

def transmit(filename):
    transmitting = getBytesOfCSV(filename)
    serialPort.write(transmitting)
    print(f"sent {len(transmitting)} bytes")
    time.sleep(3)

def broken_cirle():
    POINTS = 2040
    RES = 255
    arr = []

    for i in range(POINTS):
        x = RES * math.sin(2 * math.pi * i / POINTS) + RES / 2
        y = RES * math.cos(2 * math.pi * i / POINTS) + RES / 2
        if x > 255 or y > 255:
            print(x,y,"shit")
        arr.extend([int(math.floor(x)),int(math.floor(y)), 0 if i%2 else 255])
    arr.extend([13,13,13])
    return arr

def circle():
    POINTS = 360
    GAP = 5

    x = np.linspace(0, POINTS, POINTS)
    sine = np.round(127 * np.sin((2*np.pi*x)/POINTS)+128)
    cos = np.round(127 * np.cos((2*np.pi*x)/POINTS)+128)

    arr = []
    count = 0
    for i in range(POINTS):

        arr.extend([int(sine[i]), int(cos[i]), 0 if i%GAP*2 > GAP and cos[i] < 128 else 255])

    arr.extend([13,13,13])

    print(arr)
    return arr

def square():
    POINTS = 255

    arr = []
    for i in range(POINTS):
        arr.extend([i,0,255])
    arr.extend([255,0,255])
    for i in range(POINTS):
        arr.extend([255,i,255])
    arr.extend([255,255,255])
    for i in range(POINTS):
        arr.extend([255-i,255,i%255])
    arr.extend([0,255,255])
    for i in range(POINTS):
        arr.extend([0,255-i,i%255])
    arr.extend([0,0,255])

    arr.extend([13,13,13])
    arr.extend([13,13,13])

    print(arr)
    return arr

def lines():
    points = 255

    delay_start = 0
    delay_end = 20
    arr = []

    for i in range(0,points,5):
        arr.extend([i, 0, 255])
    arr[-1] = 0
    # arr.extend([255, 0, 0])
    for _ in range(delay_start):
        arr.extend([255, 0, 0])

    for _ in range(delay_end):
        arr.extend([0, 255, 0])

    for i in range(0,points,5):
        arr.extend([i, 255, 255])
    
    arr[-1] = 0
    
    for _ in range(delay_start):
        arr.extend([255, 255, 0])

    for _ in range(delay_end):
        arr.extend([0, 0, 0])

    arr.extend([13,13,13])
    print(arr)
    return arr


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
# turn laser ON/OFF
    elif (userInput == "ON"):
        serialPort.write(bytearray([13,13,255,13,13,13]))
    elif (userInput == "OFF"):
        serialPort.write(bytearray([0,0,0,13,13,13]))
    elif (userInput == "circle"):
        serialPort.write(bytearray(broken_cirle()))
    elif (userInput == "square"):
        serialPort.write(bytearray(square()))
    elif (userInput == "lines"):
        serialPort.write(bytearray(lines()))
    elif (userInput == "pause"):
        serialPort.write(bytearray([0,13,13,13]))
    elif (userInput[:5] == "send "):
        print(userInput[5:])
        transmit(userInput[5:])
    elif (userInput[:5] == "byte "):
        arr = list(map(int, userInput[5:].split()))
        bytes = bytearray(arr + [13,13,13])
        serialPort.write(bytes)

    else:
        serialPort.write(str.encode(userInput, "ascii"))


