#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     googlebookmarkanylyze
# Description :
#   Author:      fan
#   date:        2017/12/28
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------


import xml.sax


class GoogleBookmarkHandler(xml.sax.ContentHandler):
    def __init__(self):
        super().__init__()
        self.currentdata = ''
        self.href = ''
        self.add_date = ''
        self.icon = ''
        self.last_modified = ''

    def startElement(self, tag, attrs):
        if tag == 'A':
            try:
                print('**********书签**********')
                href = attrs['HREF']
                add_date = attrs['ADD_DATE']
                icon = attrs['ICON']
                print('href: ', href)
                print('add_date: ', add_date)
                print('icon: ', icon)
            except:
                pass
        if tag == 'H3':
            try:
                print('*********文件夹**********')
                add_date = attrs['ADD_DATE']
                last_modified = attrs['LAST_MODIFIED']
                print('add_date: ', add_date)
                print('last_modified: ', last_modified)
            except:
                pass

    def endElement(self, tag):
        pass

    def characters(self, content):
        print(content)


if __name__ == '__main__':
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    handler = GoogleBookmarkHandler()
    parser.setContentHandler(handler)

    parser.parse('bookmarks_2017_12_28.html')