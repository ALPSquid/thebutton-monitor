""" Really basic gatttool (BlueZ) wrapper

Based on https://github.com/stratosinc/pygatt
Part of https://github.com/ALPSquid/thebutton-monitor
"""

import pexpect


class connect():
    """ Use to initiate a connection to a GATT device
    Example: bt_device = gatt.connect('AB:CD:EF:01:23:45')
    """
    def __init__(self, address):
        self.address = ""  # Connected bluetooth device address. Assigned from connect()
        self.conn = None  # pexpect.spawn() object for the gatttool command
        self.connect(address)

    def connect(self, address, adapter='hci0'):
        """ Open an interactive connection to a bluetooth device

        :param address: Bluetooth device address
        :param adapter: Bluetooth adapter to use. Default: hci0
        """
        if self.conn is None:
            self.address = address
            cmd = ' '.join(['gatttool', '-b', address, '-i', adapter, '-I'])
            self.conn = pexpect.spawn(cmd)
            self.conn.expect(r'\[LE\]>', timeout=1)
            self.conn.sendline('connect')
            try:
                self.conn.expect(r'Connection successful', timeout=10)
                print("Connected to " + address)
            except pexpect.TIMEOUT:
                raise Exception("Unable to connect to device")
        else:
            raise Exception("Device already connected! Call disconnect before attempting a new connection")

    def reconnect(self):
        """ Check and attempt to reconnect to device if necessary
        :return: True if a reconnect was performed
        """
        try:
            self.conn.expect(r'Disconnected', timeout=0.1)
            self.conn.sendline('connect')
            try:
                self.conn.expect(r'Connection successful', timeout=10)
                print("Reconnected to device: " + self.address)
            except pexpect.TIMEOUT:
                # Continue and try to reconnect next time
                print("Lost connection to device: " + self.address)
            return True
        except pexpect.TIMEOUT:
            # No need to reconnect
            return False

    def disconnect(self):
        """ Disconnect from current bluetooth device """
        if self.conn is not None:
            self.conn.sendline('exit')
            self.conn = None
            print("Disconnected from " + self.address)

    def write(self, handle, value):
        """ Write a value to the specified handle

        :param handle: address to write to. e.g. 0016
        :param value: value to write
        """
        self.send(' '.join(['char-write-cmd', '0x'+handle, value]))

    def read(self, handle):
        """ Read from the specified handle

        :param handle: address to read from. e.g. 0016
        """
        self.send('char-read-hnd 0x' + handle, r'descriptor: .* \r', timeout=5)
        val = ' '.join(self.conn.after.decode("utf-8").split()[1:])
        return val

    def send(self, cmd, expect=None, timeout=5):
        """ Send command to device. Attempt a reconnect if disconnected

        :param cmd: Command to send
        """
        self.conn.sendline(cmd)
        if expect is not None:
            try:
                self.conn.expect(expect, timeout)
            except pexpect.TIMEOUT:
                if self.reconnect():
                    self.conn.sendline(cmd)
        else:
            if self.reconnect():
                self.conn.sendline(cmd)