import time
import serial
from threading import Thread

class PSoCBridge:
    serial_port: serial.Serial
    read_thread: Thread

    TERMINATOR = [13,13,13]

    def __init__(self):
        '''
        Initialises communication between PC and PSoC. Tries COM1 to COM5
        '''
        connected = False
        for i in range(5):
            try:
                self.connect(f"COM{i}")
                connected = True
                break
            except serial.SerialException:
                continue
        
        if (not connected):
            raise FileNotFoundError("Could not find an open COM port")
        


    def connect(self, comPort):
        '''
        Initialises communication between PC and PSoC
        Args:
            comPort (string): ComPort name e.g. "COM5"
        '''
        # create serial Port
        self.serial_port = serial.Serial(
            port=comPort, baudrate=1500000, bytesize=serial.EIGHTBITS, timeout=0, stopbits=serial.STOPBITS_ONE,parity=serial.PARITY_NONE
        )


        # Async port reader
        def read_serial():
            '''
            Reads ComPort and prints to console
            '''
            while 1:
            # Read data out of the buffer until a carraige return / new line is found
                #serialString = serialPort.read_until(expected="\n", size=10)

                serialString = self.serial_port.readline()
                if serialString:
                    try:
                        print(serialString.decode("ascii"))
                    except:
                        print(serialString)


        read_thread = Thread(target = read_serial)
        read_thread.daemon = True
        read_thread.start()


    def write(self, data):
        '''
        Write bytes to the PSoC (also adds terminator)
        '''
        self.write_unterminated(data + self.TERMINATOR)

    def print(self, text):
        '''
        Unused. Only sends characters to the PSoC
        '''
        self.write_unterminated(str.encode(text, "ascii"))

    def write_unterminated(self, data):
        '''
        Writes bytes to PSoC (unterminated)
        '''
        data = bytearray(data)
        self.serial_port.write(data)
        print(f"sent {len(data)} bytes")

    def speed_test(self):
        '''
        Runs a speed test
        '''
        REPEATS = 50
        DATA_LEN = 1000
        # send frames
        start = time.perf_counter()
        for i in range(0,REPEATS):
            self.write([i for i in range(1,DATA_LEN-3)])
        self.write([0])

        # wait for ACK
        while 1:
            serial_string = self.serial_port.readline()
            if serial_string:
                print(serial_string.decode("ascii"))
                break

        stop = time.perf_counter()
        elapsed = stop - start
        num_bytes = REPEATS*DATA_LEN
        print(f"recieved {REPEATS} frames ({num_bytes} bytes) in {elapsed:0.4f} seconds ({num_bytes*8/elapsed/1000:0.0f} Kbps)")