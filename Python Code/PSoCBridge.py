import serial
from threading import Thread

def Initialise(comPort):
    '''
    Initialises communication between PC and PSoC
    Args:
        comPort (string): ComPort name e.g. "COM5"
    '''
    # create serial Port
    serialPort = serial.Serial(
        port=comPort, baudrate=1500000, bytesize=serial.EIGHTBITS, timeout=0, stopbits=serial.STOPBITS_ONE,parity=serial.PARITY_NONE
    )


    # Async port reader
    def readSerial():
        '''
        Reads ComPort and prints to console
        '''
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


def sendBytes(data):
    data = bytearray(data + [13,13,13])
    serialPort.write(data)
    print(f"sent {len(data)} bytes")
