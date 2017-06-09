#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywinauto import application
# 调用模块和函数
import time


def connect_app(apppath, apptitle='', appclassname=''):
    """连接到windows应用程序"""

    app = application.Application()
    app.start(apppath)
    # 开启应用
    time.sleep(2)
    # 延时
    mainwindow = app.window_(title=apptitle, class_name=appclassname)
    mainwindow.print_control_identifiers()
    # 连接主窗口 打印主窗口下所有控件信息
    return mainwindow


def show_menu_bar(mainwindow):
    """遍历程序窗口菜单栏，注意返回对象的结构"""
    menu = mainwindow.MenuItems()

    for i in menu:
        # 输出一级菜单
        # print(i, '\n', i['text'], '\n', i['menu_items']['menu_items'])
        print(i['text'])
        for m in i['menu_items']['menu_items']:
            # 输出二级菜单
            # print(m, '\n', m['text'])
            print('\t', m['text'])


def type_words(mainwindow, words, lineid=0):
    """在Edit控件中输入和显示相关信息"""
    editor = mainwindow.window_(class_name="Edit")
    print(type(editor))
    editor.SetText(words)
    a = editor.LineCount()
    b = editor.GetLine(lineid)
    c = editor.LineLength(lineid)
    print("""\
    文本行数： %d
    获取行:   %d
    内容:     %s
    字符数:   %d""" % (a, lineid, b, c))


def about_txt(mainwindow):
    """菜单命令-关于窗口"""
    about = mainwindow.window_(title_re=u'关于“记事本”')
    time.sleep(1)
    about.print_control_identifiers()
    about.window_(title_re=u'确定').click()
    time.sleep(1)
    return


def save_file(mainwindow, savepath):
    mainwindow.MenuSelect(u'文件(&F) ->保存(&S)')
    time.sleep(.2)
    save = mainwindow.window_(title_re='另存为', class_name='#32770')
    save[u'另存为'][u'Edit'].TypeKeys(savepath)
    save[u'另存为'][u'保存'].Click()


if __name__ == '__main__':

    app_path = 'notepad.exe'
    app_title = "无标题 - 记事本"
    app_class_name = "Notepad"
    main_window = connect_app(app_path, app_title, app_class_name)
    time.sleep(1)
    type_words(main_window, u'这是一个pywinauto测试demo')
    # time.sleep(1)
    # show_menu_bar(main_window)
    save_file(main_window, r'C:\Users\fan\Desktop')
    time.sleep(1)
