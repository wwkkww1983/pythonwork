#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: sort_out_json
# Author:    fan
# date:      2018/5/14
# -----------------------------------------------------------

import json


fpath = "E:\MyWorkPlace\pythonwork\devices\google_bookmarks_soutout\Bookmarks_no_record.json"
fpath = "E:\MyWorkPlace\pythonwork\devices\google_bookmarks_soutout\Bookmarks_simple.json"


class BookMarks(object):
    def __init__(self, bookmk_path):
        self.path = bookmk_path
        self.jsondict = self.json2dict()

    def json2dict(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            dict_json = json.loads(f.read())
            return dict_json

    def printjsondict(self, a_dict):
        for k, v in a_dict.items():
            if isinstance(v, dict):
                print(k+':')
                for k1, v1 in v.items():
                    if isinstance(v1, dict):
                        print(" "*4,k1+':')
                        for k2, v2 in v1.items():
                            if isinstance(v2, dict):
                                print(" "*8,k2+':')
                                for k3, v3 in v2.items():
                                    if isinstance(v3, dict):
                                        print(" "*12,k2 + ':')
                                    elif isinstance(v3, list):
                                        print(' ')
                                    else:
                                        print(" "*12, k3, ":", v3)
                            elif isinstance(v2, list):
                                print(" "*8, k2+':')
                                for i in v2:
                                    print("            ", i)
                            else:
                                print(" "*8, k2, ":", v2)
                    elif isinstance(v1, list):
                        pass
                    else:
                        print(" "*4, k1, ":", v1)
            elif isinstance(v, list):
                pass
            else:
                print(k, ":", v)


if __name__ == '__main__':
    bm = BookMarks(fpath)
    # print(bm.jsondict)
    bm.printjsondict(bm.jsondict)
