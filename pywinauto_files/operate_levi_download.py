#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywinauto import application  #调用模块和函数
import time


if __name__ == '__main__':
    app_path = r'C:\Program Files\LeviStudio\Download.exe'
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

    load_file = download.window_(title_re='打开',class_name='#32770')
    load_file.window_(title='', class_name='Combobox').windwo_(class_name='Edit').TypeKeys(
        r'C:\Users\fan\OneDrive\pythonwork\pywinauto_files\NewProject.hmt'
    )
    # download.window_(title=u'关闭(&C)').click()






















