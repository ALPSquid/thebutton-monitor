
""" Provides access to the /r/thebutton button.
Uses a websocket.WebSocketApp to update the time, total clicks and other relevant data

Based on https://github.com/mfontanini/thebutton
Part of https://github.com/ALPSquid/thebutton-monitor
"""

from enum import Enum
import websocket
import threading
import re
import urllib.request
import json
import time
import math


class Keys(Enum):
    """ Dictionary keys used by /r/thebutton websocket response
    Sample: {"type": "ticking", "payload": {"participants_text": "756,790", "tick_mac": "fca61e446b32ba0c2851d564b413d7c953e92690", "seconds_left": 36.0, "now_str": "2015-04-16-11-33-26"}}
    """
    PAYLOAD = "payload"
    SECONDS = "seconds_left"
    PARTICIPANTS = "participants_text"
    TIME = "now_str"
    MAC = "tick_mac"


class TheButton():
    """ Represents the /r/thebutton button.
    Uses a websocket.WebSocketApp to update the time, total clicks and other relevant data
    """
    ws_re = re.compile('(wss://wss.redditmedia.com/thebutton\?h=[0-9a-f]*&e=[0-9a-f]*)')

    @staticmethod
    def _get_websocket_url():
        """ Get the websocket url from the /r/thebutton source
        :return: websocket url
        """
        req = urllib.request.urlopen("https://www.reddit.com/r/thebutton")
        contents = req.read().decode("utf-8")

        matches = TheButton.ws_re.findall(contents)
        if any(matches):
            return matches[0]
        else:
            raise Exception("Failed to find websocket url")

    def __init__(self):
        self.ws_url = self._get_websocket_url()
        self.wsa = websocket.WebSocketApp(self.ws_url, header=["User-Agent: /r/thebutton python API"],
                                          on_message=self.on_message, on_error=self.on_error)
        self._wsa_proc = None  # WSA run_forever thread

        self.base_time = 60.0  # Current button time (no milliseconds, use current_time for time with millis)
        self.last_time = self.base_time  # Button time prior to each update. Used to determine if a new record was set
        self.lowest_time = 60.0  # Lowest button time this session (no milliseconds)
        self.participants = 0  # Number of button clicks
        self.last_timestamp = ""  # Last update from server
        self._last_tick = time.perf_counter()  # Used by current_time to calculate milliseconds

    @property
    def current_time(self):
        """
        The Reddit websocket sends updated information every second (on each button time change).
        The current time since the last message is used to calculate the current milliseconds.

        :return: Current button time with milliseconds
        """
        time_diff = time.perf_counter() - self._last_tick  # Time since last update
        return self.base_time - (math.ceil((1 - time_diff) * 100) / 100.0)

    @property
    def colour(self):
        """ Colours configured for PlayBulb Candle
        :return: Flair colour for current button time
        """
        if self.base_time < 12: return '20ff0000'  # red
        if self.base_time < 22: return 'f0ff0f00'  # orange
        if self.base_time < 32: return 'ffffff00'  # yellow
        if self.base_time < 42: return '0000ff00'  # green
        if self.base_time < 52: return '0000f0ff'  # blue
        return '00ff00f0'  # purple

    def on_message(self, wsa, message):
        """ WebSocketApp message callback
        Update button attributes: base_time, lowest_time, participants, last_timestamp

        :param wsa: WebSocketApp instance
        :param message: message from socket
        """
        payload = json.loads(message)[Keys.PAYLOAD.value]
        # Update button time
        self.last_time = self.base_time
        self.base_time = payload[Keys.SECONDS.value]
        if self.base_time == 60.0 and self.last_time < self.lowest_time:
            self.lowest_time = self.last_time

        # Update participants
        participants = payload[Keys.PARTICIPANTS.value]
        if self.participants != participants:
            self.participants = participants

        # Update timestamp
        self.last_timestamp = payload[Keys.TIME.value]

        # Used to calculate button milliseconds
        self._last_tick = time.perf_counter()

    def on_error(self, wsa, error):
        """ WebSocketApp error callback
        Print the error message

        :param wsa: WebSocketApp instance
        :param error: error message
        """
        print(error)

    def start(self):
        """ Start the WebSocketApp """
        self._wsa_proc = threading.Thread(target=self.wsa.run_forever)
        self._wsa_proc.start()

    def close(self):
        """ Stop the WebSocketApp """
        self.wsa.close()
        self._wsa_proc.join()
        print("Disconnected from The Button")