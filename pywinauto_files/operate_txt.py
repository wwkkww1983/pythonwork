#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pywinauto import application
# 调用模块和函数
import time


def connect_app(apppath):
    """连接到windows应用程序"""
    app = application.Application()
    app.start(apppath)
    # 开启应用
    time.sleep(1)
    # 延时
    return app


def getmainwindow(app, apptitle, appclassname):
    mainwindow = app.window(title=apptitle, class_name=appclassname)
    mainwindow.Maximize()
    # mainwindow.print_control_identifiers()
    # 连接主窗口 打印主窗口下所有控件信息
    return mainwindow


def show_menu_bar(mainwindow):
    """遍历程序窗口菜单栏，注意返回对象的结构"""
    menu = mainwindow.MenuItems()
    for i in menu:
        # 输出一级菜单
        print(i, '\n', i['text'], '\n', i['menu_items']['menu_items'])
        print(i['text'])
        for m in i['menu_items']['menu_items']:
            # 输出二级菜单
            # print(m, '\n', m['text'])
            print('\t', m['text'])


def type_words(mainwindow, words, lineid=0):
    """在Edit控件中输入和显示相关信息"""
    elem_editor = mainwindow["Edit"]
    print(type(elem_editor))
    elem_editor.SetText(words)
    time.sleep(1)
    a = elem_editor.LineCount()
    b = elem_editor.GetLine(lineid)
    c = elem_editor.LineLength(lineid)
    print("""\
    文本行数： %d
    获取行:   %d
    内容:     %s
    字符数:   %d""" % (a, lineid, b, c))


def about_txt(appp, mainwindow):
    """菜单命令-关于窗口"""
    mainwindow.MenuSelect(u'帮助(&H) ->关于记事本(&A)')
    win_about = appp[u'关于“记事本”']
    time.sleep(1)
    # win_about.print_control_identifiers()
    win_about[u'确定'].Click()
    time.sleep(1)
    return


def save_file(appp, mainwindow, savepath):
    mainwindow.MenuSelect(u'文件(&F) ->保存(&S)')
    time.sleep(.2)
    win_save = appp[u'另存为']
    # win_save.print_control_identifiers()

    win_save[u'Edit1'].TypeKeys(savepath)
    time.sleep(.5)
    win_save[u'保存'].DoubleClick()
    time.sleep(.5)
    try:
        appp[u'确认另存为'][u'是(&Y)'].Click()
        print('已覆盖原文件')
    except Exception:
        print('已创建新文件')
        pass
    time.sleep(1)


def close(appp):
    try:
        appp['Notepad'].Close()
    except Exception:
        pass

if __name__ == '__main__':
    app_path = 'notepad.exe'
    app_title = "无标题 - 记事本"
    app_class_name = "Notepad"
    appp = connect_app(app_path)
    main_window = getmainwindow(appp, app_title, app_class_name)
    # show_menu_bar(main_window)
    # about_txt(appp, main_window)
    time.sleep(1)
    type_words(main_window, u'这是一个pywinauto测试demo')
    save_file(appp, main_window, r'C:\Users\fan\Desktop\demo.txt')
    time.sleep(1)
    close(appp)
