#!usr/bin/env python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: parse_google_bookmark.py
# Author:    fanch
# date:      2018/10/28
# -----------------------------------------------------------
import os
import time
import pyautogui


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


def del_bookmark():
    time.sleep(5)
    for i in range(50):
        pyautogui.click(x=217, y=97, clicks=1, button='right')
        time.sleep(.1)
        pyautogui.hotkey('D')
        time.sleep(.1)


if __name__ == "__main__":
    pass
    # 主功能实现：从旧书签文件中获取所有连接，去除重复连接，生成新的书签文件
    # html_lines = get_html("bookmarks_2018_10_28.html")
    # new = set_html(html_lines, "new.html")
    del_bookmark()
