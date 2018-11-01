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
    # 获取书签文件并解析成列表，每行为一个列表元素
    if not os.path.exists(html_path):
        return None
    else:
        with open(html_path, "r", encoding="utf-8") as f:
            return f.readlines()


def set_html(lines, html_path):
    # 解析：遍历列表每一个元素（字符串），不包含链接则原样排列到新列表，包含链接则判断：若链接第一次出现则存放到链接列表中同时
    # 原样排列到新列表；若链接不是第一次出现则不处理，直到遍历完整个列表
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
    # 利用pyautogui模块函数实现鼠标右击和键盘输入字母键实现浏览器书签栏书签删除
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
