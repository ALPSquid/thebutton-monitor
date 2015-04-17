# The Button Python Client

A simple library for querying the /r/thebutton button.  
Includes a gatttool wrapper for interacting with bluetooth devices.

### [Bluetooth Example](https://github.com/ALPSquid/thebutton-monitor/blob/master/src/examples/bluetooth_example.py)
#### [In Action](https://gfycat.com/FrankCorruptJackal)

### [Philips Hue Example](https://github.com/ALPSquid/thebutton-monitor/blob/master/src/examples/hue_example.py)
Example that allows you to control your hue lights according to the button timer!
####[In Action](https://gfycat.com/CheapPopularAustraliankestrel)

### thebutton.py
A WebSocketApp that automatically updates relevant button data.  
Based on [https://github.com/mfontanini/thebutton](https://github.com/mfontanini/thebutton)

#### Requirements
- Python 3
- [websocket-client](https://pypi.python.org/pypi/websocket-client)


### gatt.py
Basic Python wrapper for BlueZ gatttool.  
Based on [https://github.com/stratosinc/pygatt](https://github.com/stratosinc/pygatt)

#### Requirements
- Linux: BlueZ (for gatttool)
- Bluetooth 4.0 adapter
- [pexpect](https://pypi.python.org/pypi/pexpect)
- Tested on Python 2.7+
