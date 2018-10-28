#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: parse_google_bookmark.py
# Author:    fanch
# date:      2018/10/28
# -----------------------------------------------------------
import os
from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time


def get_html(html_path):
    if not os.path.exists(html_path):
        return None
    else:
        with open(html_path, "r", encoding="utf-8") as f:
            return f.readlines()


def set_html(lines, html_path):
    new_lines = []
    hrefs = []
    for line in lines:
        if "<DT><A HREF=" not in line:
            print(line)
            new_lines.append(line)
        else:
            if line.strip() not in hrefs:
                hrefs.append(line.strip())
                new_lines.append(line)
                print(line)
    with open(html_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    return new_lines


if __name__ == "__main__":
    # html_lines = get_html("bookmarks_2018_10_28.html")
    # new = set_html(html_lines, "new.html")
    mouse = PyMouse()
    keyboard = PyKeyboard()
    time.sleep(5)
    for i in range(200):
        mouse.click(217, 97, 2, 1)
        time.sleep(.1)
        keyboard.type_string("D")
        time.sleep(.1)
