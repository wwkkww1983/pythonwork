# coding:utf-8

from pywinauto import application
import time
import xlrd

import pyperclip     
import pyautogui


apppath = r"C:\PIStudio\HMIEditor.exe"            # 应用程序路径
exceldir = r'C:\bugs.xlsx'      # 用例输入路径
proj = u'C:\HMIProject\HMIProject.pi'    # 工程路径
#unmber_list=[335,346,358,370,382,395,407,418,430,442,454,467]
shebeilist = []
xieyilist = []
xuanz = '正常'   # 以太网 需改
class AutoDownload():
    def __init__(self):
        app = application.Application()
        self.pi = app.start(apppath)
        time.sleep(3)
        pyautogui.moveTo(42, 85)         # "打开工程"按键位置
        pyautogui.click(button='left')   # 点击,right可以不写就是左键
        self.open = self.pi.window_(title_re=u"打开", class_name ="#32770")   # 打开界面
        # self.open.print_control_identifiers()
        self.open.ConboBoxEx32.ComboBox.Edit.TypeKeys(proj)                   # 打开界面下的edit
        time.sleep(1)
        pyautogui.moveTo(1024, 679)    #"打开"工程打开
        pyautogui.click(button='left')
        time.sleep(1)
        pyautogui.moveTo(131, 39)    #"系统配置"
        pyautogui.click(button='left')
        time.sleep(1)
		
    def txkpz(self):
        pyautogui.moveTo(46,62)    #"通讯口配置"
        pyautogui.click(button='left')
        time.sleep(2)
        pyautogui.moveTo(632,303)    #"更改连接"
        pyautogui.click(button='left')
        time.sleep(1)

    def zxsblx(self, lpos, xpos):      # 选择协议
        try:
            pyautogui.moveTo(576,lpos)    #"设备类型"wecon
            pyautogui.click(button='left')
            time.sleep(1)

            pyautogui.moveTo(802,xpos)    #"协议"
            pyautogui.click(button='left')
            time.sleep(1)
        except e:
            print "dd" + str(lpos) + "ss" + str(xpos)
            pass
        #p.gcby()
        #p.lxmn()
        #p.zxmn()

    def getxxx(self,xuanze, sheb, xiey):
        wind = self.pi.window_(title_re=u"通讯设备", class_name ="#32770")
        if xuanz == '以太网':
            wind.ListBox1.Select('Ethernet')
        wind.ListBox3.Select(sheb)
        wind.ListBox2.Select(xiey)
        
		
    def qrxy(self):
        pyautogui.moveTo(658,555)    #"确定"
        pyautogui.click(button='left')
        time.sleep(1)
        pyautogui.moveTo(696,478)    #"是"
        pyautogui.click(button='left')
        time.sleep(1)
        pyautogui.moveTo(643,729)    #"确定修改"
        pyautogui.click(button='left')
        time.sleep(1)
		
    def gcby(self):
        pyautogui.moveTo(908,64)    #"工程编译"(768,62) 838
        pyautogui.click(button='left')
        time.sleep(5)
    def lxmn(self):
        pyautogui.moveTo(958,64)    #"离线模拟"(838,64)
        pyautogui.click(button='left')
        time.sleep(5)
        pyautogui.moveTo(1097,199)    #"关闭"
        pyautogui.click(button='left')
        time.sleep(2)
    def zxmn(self):
        pyautogui.moveTo(958,86)    #"在线模拟"
        pyautogui.click(button='left')
        time.sleep(5)
		
        pyautogui.moveTo(664,565)    #"OK"
        pyautogui.click(button='left')
        time.sleep(2)
        pyautogui.moveTo(1097,199)    #"关闭"
        pyautogui.click(button='left')
        time.sleep(1)
       #对列表里面匹配的内容进行结果写入操作   

    def readexcel(self):
        data = xlrd.open_workbook(exceldir)
        table = data.sheets()[0]
        nrows = table.nrows
        for i in range(nrows):
            if i == 0:
                continue                                
            shebeilist.append(table.row_values(i)[0])   
            xieyilist.append(table.row_values(i)[1])   

    def writeresult(a,b):   #编译 结果记录
        rb=xlrd.open_workbook(exceldir)
        rs=rb.sheet_by_index(0)   #通过sheet_by_index()获取的sheet:通过索引得到第一张表单，也可以通过名字：rs = rb.sheet_by_name(u'Sheet1')
        row=lb.index(a)
        wb=copy(rb)
        ws=wb.get_sheet(0)        #通过get_sheet()获取的sheet
        if b==1:
            ws.write(row+1, 2, u"编译顺利完成，可以下载或模拟运行了！") 
        elif b==0:
            ws.write(row+1, 2, u"请更正错误或警告，以保证程序正确运行！（双击错误或者警告可以跳转到相应位置）")
        elif b==2: 
            ws.write(row+1, 2, u"未知错误")   
        elif b==3:
            ws.write(row+1, 2, u"编译顺利完成，可以下载或模拟运行了！") 
        elif b==4:
            ws.write(row+1, 2, u"请更正错误或警告，以保证程序正确运行！（双击错误或者警告可以跳转到相应位置）")
        elif b==5: 
            ws.write(row+1, 2, u"未知错误")   
        elif b==6:
            ws.write(row+1, 2, u"请更正错误或警告，以保证程序正确运行！（双击错误或者警告可以跳转到相应位置）")
        elif b==7: 
            ws.write(row+1, 2, u"未知错误")   
        elif b==8:
            ws.write(row+1, 2, u"编译顺利完成，可以下载或模拟运行了！") 
        elif b==9:
            ws.write(row+1, 2, u"请更正错误或警告，以保证程序正确运行！（双击错误或者警告可以跳转到相应位置）")
        elif b==10: 
            ws.write(row+1, 2, u"未知错误")  
        wb.save(exceldir)



if __name__ == '__main__':
    p = AutoDownload()
    p.readexcel()   #读excel
    for i in range(0,len(shebeilist)):
        p.txkpz()
        p.getxxx(xuanz,shebeilist[i], xieyilist[i])
        p.qrxy()
        p.gcby()   #编译
		
#        output = self.pi.window_(title_re=u"编译输出", class_name ="Afx:ControlBar:ea0000:8:10003:10")
#        wind.SysListView32()
#        p.writeresult(i+1,output)

        p.lxmn()   #离线模拟
        #try:
            #wiplc = self.pi.window_(title_re=u"Error", class_name ="#32770")
            #wiplc.Select('LoadPlcDrivers Error, ErrorCode = 14001')
            
		#except e:
            #pass

        p.zxmn()   #在线模拟
            #try:
                #p.qrxy()
            #except e:
                #pass
    #p.txkpz()
    #p.getxxx(u'Siemens 西门子', 'Siemens S7-300 (with PC Adaptor)')
