# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
# -*- coding: utf-8 -*-
#!/usr/bin/env python 
#coding=utf-8 
import time,os,sys
from pywinauto import application

app = application.Application()
down = app.start(r"C:\PIStudio\Download.exe")#--------------------
i=0
# j=0
# k=0
# N=65536
class LogicA():
    def download(self):
        down1 = down.window_(class_name = '#32770')
# down1.print_control_identifiers()#打印download窗口所有控件类型
# down1.click()
        time.sleep(1.5) 
        # usb=down1.window_(title_re = "USB:Download", class_name = "ComboBox")
    # except:
        # time.sleep(.5)
        down1 = down.window_(class_name = '#32770')
        about_dlg=down1.window_(title_re = "PC-->HMI", class_name = "Button")
        about_dlg.click()
        time.sleep(1.5)

        project=r"E:\download.wmt"
        dd = down.window_(title_re = "打开", class_name = "#32770")
#dd.ComboBoxEx32.ComboBox.Edit.TypeKeys(project) #输入工程路径
#app[u'保存数据'][u'Edit'].SetText(name)  # 输入文件名
#app[u'保存数据'].ClickInput(coords=(560,445))
#app[u'打开'][u'ComboBox'].SetText(project)
        app[u'打开'][u'Edit'].SetText(project)
#app[u'打开'][u'打开'].click()
        time.sleep(2)
        app[u'打开'].ClickInput(coords=(556,442))
#dd.ClickInput(coords=(55,442))   #认坐标  注！此处输入的坐标的实际值为相对位置（最上层对话框的相对坐标）
        time.sleep(15)
# try:
    # down3 = down.window_(title_re = "Download", class_name = '#32770')
    # about3_dlg=down3.window_(title_re = "确定", class_name = "Button")#检查版本失败
    # about3_dlg.click()
    # time.sleep(.5)
# except:
    #time.sleep(15)
        # try:
            # down9 = down.window_(class_name = '#32770')
        # except:
            # time.sleep(1)
# about7_dlg=down9.window_(title_re = "关闭", class_name = "Button")#关闭download工具
# about7_dlg.click()
        app[u''][u'确定'].click()
        #app[u''][u'取消'].click()
        time.sleep(30)
        #app[u''][u'确定'].click()
        #app[u''][u'取消'].click()
        #time.sleep(35)



    def downloadd(self):
        down1 = down.window_(class_name = '#32770')
# down1.print_control_identifiers()#打印download窗口所有控件类型
# down1.click()
        time.sleep(.5)
    # try:
        # usb=down1.window_(title_re = "USB:Download", class_name = "ComboBox")
    # except:
        # time.sleep(.5)
        down1 = down.window_(class_name = '#32770')
        about_dlg=down1.window_(title_re = "PC-->HMI", class_name = "Button")
        about_dlg.click()
        time.sleep(1)
        project=r"E:\download.wmt"#--------------------------------------------------------------
        dd = down.window_(title_re = "打开", class_name = "#32770")
#dd.ComboBoxEx32.ComboBox.Edit.TypeKeys(project) #输入工程路径
#app[u'保存数据'][u'Edit'].SetText(name)  # 输入文件名
#app[u'保存数据'].ClickInput(coords=(560,445))
#app[u'打开'][u'ComboBox'].SetText(project)
        app[u'打开'][u'Edit'].SetText(project)
#app[u'打开'][u'打开'].click()
        time.sleep(1)
        app[u'打开'].ClickInput(coords=(556,442))
#dd.ClickInput(coords=(55,442))   #认坐标  注！此处输入的坐标的实际值为相对位置（最上层对话框的相对坐标）
        time.sleep(9)
# try:
    # down3 = down.window_(title_re = "Download", class_name = '#32770')
    # about3_dlg=down3.window_(title_re = "确定", class_name = "Button")#检查版本失败
    # about3_dlg.click()
    # time.sleep(.5)
# except:
    # time.sleep(1)
        try:
            down9 = down.window_(class_name = '#32770')
        except:
            time.sleep(1)
# about7_dlg=down9.window_(title_re = "关闭", class_name = "Button")#关闭download工具
# about7_dlg.click()
        #app[u''][u'确定'].click()
        app[u''][u'取消'].click()
        time.sleep(1)
# if __name__ == '__main__':
    # p=LogicA()
    # while i < N:
        # if j<5:
            # p.downloadd()
            # k=k+1S
            # print k			
            # j=j+1S
        # else:
            # p.download()
            # k=k+1
            # print "long"
            # print k
            # j=0
            # continue			
        # i=i+1
if __name__ == '__main__':
    p=LogicA()
    while 1:
        p.download()			
        i=i+1
        print i