#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: seq_in_rows_and_cols
# Author:    fan
# date:      2018/2/9
# -----------------------------------------------------------
if __name__ == '__main__':
    #
    ncount = 110
    nrow = 22
    ncol = 5
    l = list(range(ncount))
    if ncount != nrow * ncol:
        print('Array counts error')
    if ncount == nrow * ncol:
        lnew = []
        for i in range(nrow):
            temp = []
            tindex = 0
            for j in range(ncol):
                if i % 2 == 0:
                    tindex = i * ncol + j
                if i % 2 == 1:
                    tindex = i * ncol + (ncol - 1 - j)
                temp.append(l[tindex])
            lnew.append(temp)
            print(temp)
    # print(ncount, nrow, ncol, l)
