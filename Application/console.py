from Utils import CSVReader, Shapes
from PSoCBridge import PSoCBridge
import time

class Console:
    def __init__(self, PSoC: PSoCBridge) -> None:
        self.PSoC : PSoCBridge = PSoC

    def transmit(self, filename):
        try:
            data = CSVReader.getBytesOfAxisCSV(filename)
            self.PSoC.write(data)
            time.sleep(3)
        except Exception as e:
            print("cannot connect to console, or file not found", e)

    def test(self):
        self.transmit("atom-500")
        self.transmit("atom-1000")
        self.transmit("circle-510")
        self.transmit("circle-2040")
        self.transmit("image-4000")
        self.transmit("image-1500")
        self.transmit("mike-750")
        self.transmit("mike-1000")

    def startConsole(self):
        while 1:
            userInput = input()
            if userInput == "speed":
                self.PSoC.speed_test()
            elif userInput == "test":
                self.test()
            elif userInput == "ON" or userInput == "on":
                self.PSoC.write([13, 13, 255] + self.PSoC.TERMINATOR)
            elif userInput == "OFF" or userInput == "off":
                self.PSoC.write([0, 0, 0] + self.PSoC.TERMINATOR)
            elif userInput == "circle":
                self.PSoC.write(Shapes.circle())
            elif userInput == "bcircle":
                self.PSoC.write(Shapes.broken_cirle())
            elif userInput == "square":
                self.PSoC.write(Shapes.square())
            elif userInput == "lines":
                self.PSoC.write(Shapes.lines())
            elif userInput == "pause":
                self.PSoC.write([0] + self.PSoC.TERMINATOR)
            elif userInput[:5] == "send ":
                print(userInput[5:])
                self.transmit(userInput[5:])
            elif userInput[:5] == "byte ":
                arr = list(map(int, userInput[5:].split()))
                bytes = arr + [self.PSoC.TERMINATOR]
                self.PSoC.write(bytes)
            elif userInput[:5] == "text ":
                print("Note: non-terminated data intended for debugging. Flush UART.")
                self.PSoC.write(str.encode(userInput, "ascii"))
            elif userInput == "quit" or userInput == "exit":
                break
            else:
                pass