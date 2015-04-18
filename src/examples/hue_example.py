# Example by kaloncheung124 (https://github.com/kaloncheung124/thebutton-monitor)

from thebutton import TheButton
from phue import Bridge
import math


b = Bridge('BRIDGE IP')
#If running for the first time, press button on bridge and run with b.connect() uncommented
b.connect()

#b.lights is a list of your light objects. I wanted to use lights 0 and 1,
# so I used b.lights[0:2].
lights = b.lights[0:2]


class HueButton():
    def __init__(self, lights):
        self.lights = lights; 
        for light in self.lights:
            light.brightness = 255
            light.transitiontime = 2

        # Create a new instance of the button client. Does nothing until start() is called
        self.the_button = TheButton()
        self.last_lowest = 60.0

    def set_color(self, hue):
        #Takes in a string for a color and sets all lights to that color
        for light in self.lights:
            light.xy = hue;

    def flash(self):
        for light in self.lights:
            light.xy = [0.2941, 0.1106]

    def run(self):
        # The WebSocketApp loop runs in it's own thread,
        # so make sure you call TheButton.close() when you're done with it!
        self.the_button.start()

        try:
            while True:
                color = self.the_button.hue_color  #Hue XY color space values
                # Set the Hue bulb to the current flair colour
                # Resource: Protocols for Hue bulbs from https://github.com/studioimaginaire/phue/
                self.set_color(color)

                # There's no built-in time persistence, so by default, lowest time is for the current session
                if self.the_button.lowest_time < self.last_lowest:
                    self.last_lowest = self.the_button.lowest_time
                    self.flash()  # Flash when a new record is set
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
    huebutton = HueButton(lights)
    huebutton.run()
