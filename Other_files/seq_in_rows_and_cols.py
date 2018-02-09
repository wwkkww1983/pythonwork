#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: seq_in_rows_and_cols
# Author:    fan
# date:      2018/2/9
# -----------------------------------------------------------
if __name__ == '__main__':
    ncount = 12
    nrow = 3
    ncol = 4
    l = list(range(ncount))
    if ncount == nrow * ncol:
        lnew = []
        for i in range(len(l)):
            if i // 2 == 0:

    print(ncount, nrow, ncol, l)
