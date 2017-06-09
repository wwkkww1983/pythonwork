#!/usr/bin/env python3
# _*_ coding: utf-8 _*_
# create on 2017.2.16
# author: fan
import serial
import binascii
import struct
import time
send_str       = 'are you ok'
send_str_b     = send_str.encode('ascii')
send_str_b_hex = binascii.b2a_hex(send_str_b)
t2             = serial.Serial('com2', 9600)
t3 			   = serial.Serial('com3', 9600)
n  	    	   = t2.write(send_str_b)
print("""
from:
com       = %s
baudrated  = %d
datasize  = %d
parity    = %s
stopbits  = %d
""" % (t2.port, t2.baudrate, t2.bytesize, t2.parity, t2.stopbits))
print("""
to:
com       = %s
baudrate  = %d
datasize  = %d
parity    = %s
stopbits  = %d
""" % (t3.port, t3.baudrate, t3.bytesize, t3.parity, t3.stopbits))
# print (t2.port,'---->',t3.port)
print("""
str send            = %s
hexadecimal data    = %s""" % (send_str, send_str_b_hex))
t2.write(send_str_b)
time.sleep(.2)
read_str = t3.read(size=n)
read_str_hex = binascii.b2a_hex(read_str)
print("""
str received        = %s
hexadecimal data    = %s""" % (read_str, read_str_hex))
