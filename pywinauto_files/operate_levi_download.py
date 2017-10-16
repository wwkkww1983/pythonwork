#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywinauto import application  #调用模块和函数
import time


if __name__ == '__main__':
    app_path = r'D:\Program Files\weconsoft\LeviStudio\20170120 发布\Download.exe'
    app = application.Application()
    app.start(app_path)
    time.sleep(1)

    download = app.window_(class_name='#32770')
    # download.print_control_identifiers()
    time.sleep(1)
    combobox_port = download.window_(title_re=u'COM1 : 通信端口', class_name='ComboBox')
    # combobox_port = download.window_(title_re=r'COM1 : 通信端口', class_name='ComboBox')
    # portselect.Select(u"COM1 : 通信端口")
    print(combobox_port.ItemTexts())

    combobox_paudrates = download.window_(title_re='115200', class_name='ComboBox')
    # combobox_paudrates.Select("9600")
    print(combobox_paudrates.ItemTexts())

    combobox_file_type = download.window_(title_re='工程文件', class_name='ComboBox')
    # combobox_file_type.Select(u"镜像文件")
    print(combobox_file_type.ItemTexts())

    # beep = download.window_(title_re=u"蜂鸣器", class_name="Button")

    button_download = download.window_(title=r'PC-->HMI(&D)', class_name='Button')
    button_download.click()
    time.sleep(1)

    # load_file = download['打开Dialog']
    load_file = app.top_window_()

    filepath_edit = load_file['文件名(&N):Edit']
    filepath_edit = load_file.
    filepathopen_button = load_file['打开(&O)']

    filepath_edit.TypeKeys(r'E:\桌面临时文件\20170916临时\NewProject\NewProject.hmt')
    filepathopen_button.click()
    time.sleep(5)
    try:
        warn = app['Warning']
        print(warn['Static2'])
        time.sleep(5)
        warn['否(&N)'].click()
    except Exception as e:
        print(e)






















