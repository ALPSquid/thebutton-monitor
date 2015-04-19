from thebutton import TheButton
import serial

class ButtonSerial():
    def __init__(self):
        self.the_button = TheButton()
    
    def init_serial(self,interface,baud):
        self.interface = serial.Serial(interface, baud, timeout=1)
 
    def run(self):
        # The WebSocketApp loop runs in it's own thread,
        # so make sure you call TheButton.close() when you're done with it!
        self.the_button.start()

        try:
            while True:
                colour = self.the_button.ascii_colour
                self.interface.write(colour.encode()) 
        except KeyboardInterrupt:
            pass
        self.close()

    def close(self):
        # The Button WebSocketApp runs in it's own thread, so make sure it's closed. This also closes the socket
        self.the_button.close()


if __name__ == "__main__":
    button_app = ButtonSerial()
    button_app.init_serial('/dev/ttyACM0',9600)
    button_app.run()
