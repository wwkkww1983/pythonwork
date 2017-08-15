# !/usr/bin/env python3
# -*- coding: utf-8 -*-

from os import getenv
import

_sqlite3.

server = getenv('PYMSSQL_TEST_SERVER')
user = getenv('PYMSSWL_TEST_USERNAME')
password = getenv('PYMSSQL_TEST_PASSWORD')

conn = pymssql.connect(server, user, password, 'tempdb')
cursor = conn.cursor()
