import ledcontroller
from thebutton import TheButton
import math

class ButtonApp():
    def __init__(self):
	CONTROLLER_ADDRESS="192.168.1.119"
	self.led = ledcontroller.LedController(CONTROLLER_ADDRESS)
	self.group = 0 #Limitless LED Bulb Bridge Group of LEDs to use. 0 is all.
        # Create a new instance of the button client. Does nothing until start() is called
        self.the_button = TheButton()
        self.last_lowest = 60.0

    def run(self):
        # The WebSocketApp loop runs in it's own thread,
        # so make sure you call TheButton.close() when you're done with it!
        self.the_button.start()
        previous_colour='0' # Initialise previous colour
        try:
            while True:
                # Colours are in hexadecimal but the PlayBulb Candle required saturation in front of the value
                colour = self.the_button.limitless_colour
                # Set the PlayBulbs to the current flair colour
                # Resource: Protocols for PlayBulb products (https://github.com/Phhere/Playbulb)
                if colour != previous_colour:
                    self.led.set_color(colour, self.group)
                    previous_colour=colour
                # There's no built-in time persistence, so by default, lowest time is for the current session
                if self.the_button.lowest_time < self.last_lowest:
                    self.led.set_color('white', self.group)  # Flash when a new record is set
                    self.led.set_color(colour, self.group)
                    self.last_lowest = self.the_button.lowest_time
                    print("New button record! " + str(math.floor(self.last_lowest)))
                    previous_colour='0' # Reset previous colour so flashing stops before next colour change
        except KeyboardInterrupt:
            pass
        self.close()

    def close(self):
        # The Button WebSocketApp runs in it's own thread, so make sure it's closed. This also closes the socket
        self.the_button.close()


if __name__ == "__main__":
    button_app = ButtonApp()
    button_app.run()

