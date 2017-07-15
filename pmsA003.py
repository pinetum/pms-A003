import serial
import time
import sys
import json
import datetime
import binascii

class pmsA003():
    def __init__(self, dev):
        self.serial = serial.Serial(dev, baudrate=9600, timeout=3)
    def __exit__(self, exc_type, exc_value, traceback):
        self.serial.close()


    def setIdel(self):
        idelcmd = b'\x42\x4d\xe4\x00\x00\x01\x73'
        ary = bytearray(idelcmd)
        self.serial.write(ary)

    def setNormal(self):
        normalcmd = b'\x42\x4d\xe4\x00\x01\x01\x74'
        ary = bytearray(normalcmd)
        self.serial.write(ary)

    def vertify_data(self):
        if not self.data:
            return False
        return True


    def read_data(self):
        while True:
            b = self.serial.read(1)
            if b == b'\x42':
                data = self.serial.read(31)
                if data[0] == b'\x4d':
                    self.data = bytearray(b'\x42' + data)
                    if self.vertify_data():
                        return self._PMdata()

    def _PMdata(self):
        d = {}
        d['time'] = datetime.datetime.now()
        d['apm25'] = self.data[6] * 256 + self.data[7]
        d['apm10'] = self.data[4] * 256 + self.data[5]
        d['apm100'] = self.data[8] * 256 + self.data[9]
        return d

if __name__ == '__main__':
    print "starting..."
    con = pmsA003('/dev/ttyAMA0')
    d = con.read_data()
    print(d)

