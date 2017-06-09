# !/usr/bin/env python3
# _*_ coding: utf-8 _*_

from struct import *


def bytesfromtoint():
    a = pack('hhl', 1, 2, 3)
    b = unpack('hhl', b'\x00\x01\x00\x02\x00\x00\x00\x03')
    c = calcsize('hhl')
    d = 0
    d = unpack('!hh', b'B661')
    print("""\
    a: {0}
    b: {1}
    c: {2}
    d: {3}""".format(a, b, c, d))

def bytestoint():
    string_hex = '32 30 30 46 31 39 30 46 37 34 30 43 37 37 30 43 ' \
                 '32 45 30 31 33 38 30 31 34 43 30 41 34 34 30 41 ' \
                 '32 41 30 38 41 41 30 36 41 41 30 37 41 41 30 36 ' \
                 '34 33 30 32 41 39 30 36 37 34 30 36 41 37 30 36 ' \
                 '33 41 35 44 35 43 30 30 33 43 33 43 45 38 46 46 ' \
                 '36 45 43 35 41 30 46 46 34 42 31 33 31 43 30 30 ' \
                 '30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 30 ' \
                 '30 30 30 30 38 32 36 32 30 31 30 30 30 30 30 30 '
    string_hex2 = '32 30 30 46 31 39 30 46 37 34 30 43 37 37 30 43 '
    string_hex2 = '42 36 36 31'
    int_list1 = []
    byte_s = bytes.fromhex(string_hex2)
    byte_list = []
    int_lsit = []
    for index in range(len(byte_s)):
        if index%2 == 0:
            byte_list.append(byte_s[index:index+2])
            if index%4 == 2:
                integer = int(byte_list[index//2]+byte_list[index//2-1], base=16)
                int_lsit.append(integer)
    print(byte_list,'\n', int_lsit)

print(bytestoint())
