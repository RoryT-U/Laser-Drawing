# pip install pyserial

import serial
import time
from threading import Thread
import random
import csv

serialPort = serial.Serial(
    port="COM5", baudrate=1500000, bytesize=serial.EIGHTBITS, timeout=0, stopbits=serial.STOPBITS_ONE,parity=serial.PARITY_NONE
)

def readCSV(filename):
  with open(filename, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    row = next(csvreader)
    if row[-1] == '':
        row = row[:-1]
    int_row = [int(value) for value in row]

    if max(int_row) > 255:
        int_row = [int(value)//16 for value in row] # is 12bits
    else:
        int_row = [int(value) for value in row]
    return int_row

def getBytesOfCSV(filename):
    x = readCSV("Python Code\\Coordinate\\converted_csvs\\"+filename+"-y.csv")
    y = readCSV("Python Code\\Coordinate\\converted_csvs\\"+filename+"-x.csv")
    points = [x,y]

    output = []
    for i in range(len(points[0])):
        output.extend([points[0][i], points[1][i], 255])

    return bytearray(output + [13,13,13])


#### READ DATA
DATA = getBytesOfCSV("circle-2040")

#DATA = bytearray([random.choice(range(255)) for _ in range(997)] + [13,13,13])


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

while 1:
    userInput = input()

    if (userInput == "data"):
        sendData()
    elif (userInput == "speed"):
        dataTest()
    elif (userInput == "pause"):
        serialPort.write(bytearray([0,13,13,13]))
    elif (userInput[:5] == "send "):
        print(userInput[5:])
        transmit(userInput[5:])
    else:
        serialPort.write(str.encode(userInput, "ascii"))



