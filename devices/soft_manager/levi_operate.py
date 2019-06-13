#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: levi_operate
# Author:    fan
# date:      2019/6/11 011
# -----------------------------------------------------------
from pywinauto import application

app = application.Application()


def set_wl_zizhuangtaixianshi_suoyouzhuangtai():
    # 字状态显示部件 设置所有状态
    app.connect(title="所有状态")
    win_suoyouzhuangtai = app["所有状态"]
    for i in range(0, 64):
        win_suoyouzhuangtai['第{}个状态：Edit'.format(str(i))].SetText("状态{}".format(str(i)))


def get_project_attrs():
    app.connect(title="工程属性")
    win_project_attrs = app["工程属性"]
    # win_project_attrs.print_control_identifiers(2)
    print(win_project_attrs["请选择HMI系列ComboBox"].ItemTexts())
    print(win_project_attrs["请选择HMI系列ComboBox"].selected_index())
    print(win_project_attrs["请选择HMI系列ComboBox"].selected_text())

    print(win_project_attrs["请选择HMI型号ComboBox"].ItemTexts())
    print(win_project_attrs["请选择HMI型号ComboBox"].selected_index())
    print(win_project_attrs["请选择HMI型号ComboBox"].selected_text())

    print(win_project_attrs["请选择通讯接口ListBox"].texts())
    print(win_project_attrs["请选择通讯接口ListBox"].get_item_focus())
    print(win_project_attrs["请选择通讯接口ListBox"].texts()[
              win_project_attrs["请选择通讯接口ListBox"].get_item_focus()
          ])

    win_project_attrs["请选择HMI系列ComboBox"].Select(0)
    print(win_project_attrs["请选择HMI系列ComboBox"].ItemTexts())
    print(win_project_attrs["请选择HMI系列ComboBox"].selected_index())
    print(win_project_attrs["请选择HMI系列ComboBox"].selected_text())

    print(win_project_attrs["请选择HMI型号ComboBox"].ItemTexts())
    print(win_project_attrs["请选择HMI型号ComboBox"].selected_index())
    print(win_project_attrs["请选择HMI型号ComboBox"].selected_text())

    print(win_project_attrs["请选择通讯接口ListBox"].texts())
    print(win_project_attrs["请选择通讯接口ListBox"].get_item_focus())
    print(win_project_attrs["请选择通讯接口ListBox"].texts()[
              win_project_attrs["请选择通讯接口ListBox"].get_item_focus()
          ])

if __name__ == '__main__':
    # set_wl_zizhuangtaixianshi_suoyouzhuangtai()
    get_project_attrs()
