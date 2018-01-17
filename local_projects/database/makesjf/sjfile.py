#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     sjfile
# Description :
#   Author:      fan
#   date:        2018/1/17
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------
import sqlite3 as sql
import os


class SJF(object):
    def __init__(self):
        self.name = ''
        self.path = ''
        self.tablelist = []
        self.cursor = None

    def get_cursor(self, dbpath):
        c = None
        try:
            conn = sql.connect(dbpath)
            c = conn.cursor()
        except:
            print('fail to connect', dbpath)
        self.path = dbpath
        self.name = os.path.split(dbpath)[1]
        self.cursor = c
        return c

    def get_tablesnames(self):
        tablesnames = []
        if self.cursor:
            c = self.cursor
            for table in c.execute("SELECT name FROM sqlite_master WHERE type='table'"):
                tablesnames.append(table[0])
        self.tablelist = tablesnames
        return tablesnames

if __name__ == '__main__':
    pass
    file = SJF()
    file.get_cursor('示教文件demo.db')
    file.get_tablesnames()
    print("""get db file:
             path: {}
             name: {}
             cursor: {}
             table list: {}""".format(file.path, file.name, file.cursor, file.tablelist))