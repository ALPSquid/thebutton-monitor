from thebutton import TheButton
import subprocess
import math


class ButtonApp():
    def __init__(self):
        # Find your BT device's address using 'hcitool lescan' (requires su)
        PLAYBULB_ADDRESS_1 = "AB:CD:EF:01:02:03"
        #PLAYBULB_ADDRESS_2 = "AB:CD:EF:01:02:03"
        #PLAYBULB_ADDRESS_3 = "AB:CD:EF:01:02:03"
	# Add bulbs to use to list
        self.bulb_list = []
        self.bulb_list.append(PLAYBULB_ADDRESS_1)
        # Create a new instance of the button client. Does nothing until start() is called
        self.the_button = TheButton()
        self.last_lowest = 60.0

    def writeColour(self, colour):
        # Set Playbulb colour
        for e in self.bulb_list:
            subprocess.call(('gatttool -b ' + e + ' --char-write -a 0x0016 -n ' + colour).split())

    def writeEffect(self, command):
        # Set Playbulb colour
        for e in self.bulb_list:
            subprocess.call(('gatttool -b ' + e + ' --char-write -a 0x0014 -n ' + command).split())

    def run(self):
        # The WebSocketApp loop runs in it's own thread,
        # so make sure you call TheButton.close() when you're done with it!
        self.the_button.start()
        previous_colour='0'
        try:
            while True:
                # Colours are in hexadecimal but the PlayBulb Candle required saturation in front of the value
                colour = '00'+self.the_button.colour
                # Set the PlayBulb to the current flair colour
                # Resource: Protocols for PlayBulb products (https://github.com/Phhere/Playbulb)
                if colour != previous_colour:
                    self.writeColour(colour)
                previous_colour=colour
                # There's no built-in time persistence, so by default, lowest time is for the current session
                if self.the_button.lowest_time < self.last_lowest:
                    self.last_lowest = self.the_button.lowest_time
                    self.writeEffect(colour+'01000100')  # Flash when a new record is set
                    print("New button record! " + str(math.floor(self.last_lowest)))
        except KeyboardInterrupt:
            pass
        self.close()

    def close(self):
        # The Button WebSocketApp runs in it's own thread, so make sure it's closed. This also closes the socket
        self.the_button.close()

if __name__ == "__main__":
    button_app = ButtonApp()
    button_app.run()

