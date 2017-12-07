#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     bintoascii
# Description :
#   Author:      fan
#   date:        2017/11/30
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------

import binascii

i1 = b'31'
b1 = b'30303031'

print('i1: ', i1, 'b1: ', b1)

b2ah = binascii.b2a_hex(i1)
a2bh = binascii.a2b_hex(b1)

print('b2ah: ', b2ah, 'a2bh: ', a2bh)

if __name__ == '__main__':
    pass
    
