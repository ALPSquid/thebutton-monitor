# The Button Python Client

A simple library for querying the /r/thebutton button.  
Includes a gatttool wrapper for interacting with bluetooth devices.

### [Bluetooth Example](https://github.com/ALPSquid/thebutton-monitor/blob/master/src/examples/bluetooth_example.py)
#### [In Action](https://gfycat.com/FrankCorruptJackal)

### [Philips Hue Example](https://github.com/ALPSquid/thebutton-monitor/blob/master/src/examples/hue_example.py)  
(Thanks to [kaloncheung124](https://github.com/kaloncheung124/thebutton-monitor))
####[In Action](https://gfycat.com/CheapPopularAustraliankestrel)

### [Arduino Example](https://github.com/ALPSquid/thebutton-monitor/blob/master/src/examples/arduino_example.py)  
(Thanks to [primehunter326](https://github.com/primehunter326/thebutton-monitor))

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
