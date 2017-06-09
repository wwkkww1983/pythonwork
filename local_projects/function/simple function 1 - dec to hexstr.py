# !/user/bin/python3
# _*_ coding: utf-8 _*_
# created on2.23,2017
# author: fan


def dec_hex_chr(x):
    # 两种情况，第一种包含"0x"; 第二种将"0x"去除
    x_hex = hex(x)
    c = ''
    for i in x_hex:
        if i != '0' and i != 'x':
            c += i
    return x_hex, c


n = int(input('Please input a integer: '))
n_hex_chr = dec_hex_chr(n)
print(n, '的16进制值表示的字符串是：', n_hex_chr)
