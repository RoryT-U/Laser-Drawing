from ast import List
import time
from jax import Array
import serial
from threading import Thread


class PSoCBridge:
    serial_port: serial.Serial
    read_thread: Thread
    datastream = []
    C_RED = 192
    C_GREEN = 48
    C_BLUE = 12
    C_ALL = 255
    C_OFF = 0

    TERMINATOR = [13, 13, 13]

    def colour(self, red, green, blue):
        return self.C_RED*red + self.C_GREEN*green + self.C_BLUE*blue

    def __init__(self, **kwargs):
        """
        Initialises communication between PC and PSoC. Tries COM0 to COM9
        """
        self.ignoreCOM = kwargs.get('ignoreCOM', False)
        self.flipX = kwargs.get('flipX', False)
        self.flipY = kwargs.get('flipY', False)

        if self.ignoreCOM:
            return

        connected = False
        for i in range(10):
            try:
                print("trying ",i)
                self.connect(f"COM{i}")
                connected = True
                break
            except serial.SerialException:
                continue

        if not connected:
            self.ignoreCOM = True
            raise print("Could not find an open COM port. Check cable and re-run the program!")

    def connect(self, comPort):
        """
        Initialises communication between PC and PSoC
        Args:
            comPort (string): ComPort name e.g. "COM5"
        """
        # create serial Port
        self.serial_port = serial.Serial(
            port=comPort,
            baudrate=1500000,
            bytesize=serial.EIGHTBITS,
            timeout=0,
            stopbits=serial.STOPBITS_ONE,
            parity=serial.PARITY_NONE,
        )

        # Async port reader
        def read_serial():
            """
            Reads ComPort and prints to console
            """
            while 1:
                # Read data out of the buffer until a carraige return / new line is found
                # serialString = serialPort.read_until(expected="\n", size=10)

                serialString = self.serial_port.readline()
                if serialString:
                    try:
                        print(serialString.decode("ascii"))
                    except:
                        print(serialString)

        self.read_thread = Thread(target=read_serial)
        self.read_thread.daemon = True
        self.read_thread.start()

    def write(self, data):
        """
        Write bytes to the PSoC (also adds terminator)
        """
        result = []
        if self.flipX or self.flipY:
            for i in range(0, len(data), 3):
                x, y, color = data[i], data[i + 1], data[i + 2]
                if self.flipX:
                    x = 255 - x
                if self.flipY:
                    y = 255 - y
                result.extend([x, y, color])
        else:
            result = data


        print(result[-6:])

        self.write_unterminated(result + self.TERMINATOR)

    def send_text(self, text):
        """
        Unused. Only sends characters to the PSoC for debugging
        """
        self.write_unterminated(str.encode(text, "ascii"))

    def write_unterminated(self, data):
        """
        Writes bytes to PSoC (unterminated)
        """
        self.datastream = data
        if self.ignoreCOM:
            print(f"COM not connected: {len(data)} bytes")
            return

        data = bytearray(data)
        self.serial_port.write(data)
        print(f"sent {len(data)} bytes")

    def get_data_stream(self):
        return self.datastream

    def speed_test(self):
        """
        Runs a speed test
        """
        REPEATS = 50
        DATA_LEN = 1000
        # send frames
        start = time.perf_counter()
        for i in range(0, REPEATS):
            self.write([i for i in range(1, DATA_LEN - 3)])
        self.write([0])

        # wait for ACK
        while 1:
            serial_string = self.serial_port.readline()
            if serial_string:
                print(serial_string.decode("ascii"))
                break

        stop = time.perf_counter()
        elapsed = stop - start
        num_bytes = REPEATS * DATA_LEN
        print(
            f"recieved {REPEATS} frames ({num_bytes} bytes) in {elapsed:0.4f} seconds ({num_bytes*8/elapsed/1000:0.0f} Kbps)"
        )
