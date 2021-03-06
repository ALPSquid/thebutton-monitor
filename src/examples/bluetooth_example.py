from thebutton import TheButton
import gatt
import math


class ButtonApp():
    def __init__(self):
        # Find your BT device's address using 'hcitool lescan' (requires su)
        PLAYBULB_ADDRESS_1 = "AB:CD:EF:01:02:03"
        #PLAYBULB_ADDRESS_2 = "AB:CD:EF:01:02:03"
        #PLAYBULB_ADDRESS_3 = "AB:CD:EF:01:02:03"
	# Add bulbs to use to list
        self.bulb_list = []
        self.bulb_list.append(gatt.connect(PLAYBULB_ADDRESS_1))
        #self.bulb_list.append(gatt.connect(PLAYBULB_ADDRESS_2))
        #self.bulb_list.append(gatt.connect(PLAYBULB_ADDRESS_3))
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
                colour = '00'+self.the_button.colour
                # Set the PlayBulbs to the current flair colour
                # Resource: Protocols for PlayBulb products (https://github.com/Phhere/Playbulb)
                if colour != previous_colour:
                    for e in self.bulb_list:
                        e.write('0016', colour)
                    previous_colour=colour
                # There's no built-in time persistence, so by default, lowest time is for the current session
                if self.the_button.lowest_time < self.last_lowest:
                    for e in self.bulb_list:
                        e.write('0014', colour+'01000100')  # Flash when a new record is set
                    self.last_lowest = self.the_button.lowest_time
                    print("New button record! " + str(math.floor(self.last_lowest)))
                    previous_colour='0' # Reset previous colour so flashing stops before next colour change
        except KeyboardInterrupt:
            pass
        self.close()

    def close(self):
        # The Button WebSocketApp runs in it's own thread, so make sure it's closed. This also closes the socket
        self.the_button.close()
        # Disconnect from the bluetooth device
        for e in self.bulb_list:
            e.disconnect()


if __name__ == "__main__":
    button_app = ButtonApp()
    button_app.run()

