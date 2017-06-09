from pywinauto import application  #调用模块和函数
import time

app= application.Application()  
#app.start("notepad.exe")  #开启应用
#time.sleep(1)  #延时1秒

#myProcess = 00140C54  #进程ID
#myHandle  = 000B0DB2  #句柄ID
#app.connect(process = myProcess)  #关联进程
#app.connect(handle = myHandle)  #关联句柄
#dlg = app.window_(title_re=u"无标题"，class_name_re="Notepad")  #通过标题和窗口类名获取窗口
dlg = app.window_(title_re=PIStudio)
