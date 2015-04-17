from thebutton import TheButton
import gatt
import math


class ButtonApp():
    def __init__(self):
        # Find your BT device's address using 'hcitool lescan' (requires su)
        self.playbulb = gatt.connect('AB:CD:EF:01:23:45')
        # Create a new instance of the button client. Does nothing until start() is called
        self.the_button = TheButton()

        self.last_lowest = 60.0


    def run(self):
        # The WebSocketApp loop runs in it's own thread,
        # so make sure you call TheButton.close() when you're done with it!
        self.the_button.start()

        try:
            while True:
                # Colours are in hexadecimal but the PlayBulb Candle required saturation in front of the value
                colour = '00'+self.the_button.colour
                # Set the PlayBulb to the current flair colour
                # Resource: Protocols for PlayBulb products (https://github.com/Phhere/Playbulb)
                self.playbulb.write('0016', colour)

                # There's no built-in time persistence, so by default, lowest time is for the current session
                if self.the_button.lowest_time < self.last_lowest:
                    self.last_lowest = self.the_button.lowest_time
                    self.playbulb.write('0014', colour+'01000100')  # Flash when a new record is set
                    print("New button record! " + str(math.floor(self.last_lowest)))
        except KeyboardInterrupt:
            pass
        self.close()

    def close(self):
        # The Button WebSocketApp runs in it's own thread, so make sure it's closed. This also closes the socket
        self.the_button.close()
        # Disconnect from the bluetooth device
        self.playbulb.disconnect()


if __name__ == "__main__":
    button_app = ButtonApp()
    button_app.run()