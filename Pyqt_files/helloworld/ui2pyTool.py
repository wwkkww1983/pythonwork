#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.ui'):
            os.system('pyuic5 -o ui_%s.py -x %s' % (file.rsplit('.', 1)[0], file))
        elif file.endswith('.qrc'):
            os.system('pyrcc5 -o %s_rc.py %s' % (file.rsplit('.', 1)[0], file))
