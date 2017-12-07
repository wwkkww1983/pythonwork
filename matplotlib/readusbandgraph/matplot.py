#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name：     matplot
# Description :
#   Author:      fan
#   date:        2017/12/1
#   IDE:         PyCharm Community Edition
# -----------------------------------------------------------
from pylab import figure, show, plt
import usbhid2 as hid
from time import ctime, sleep
import logging as log
import threading
log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')

global values

def draw(data1, data2):
    figname = data1['图表名称']
    xname = data1['采样时间']
    xtickvalue = data1['time']
    dataname = data1['数据名称']
    yvalues = [n for n in data2]

    fig = figure(figsize=(12, 6), dpi=80)
    ax = fig.add_subplot(1, 1, 1)
    x = [i for i in range(501)]
    y = yvalues + [0]

    ax.plot(x, y, 'b.-', label=dataname, linewidth=1)
    ax.set_xlabel(xname)
    ax.set_xticks([0, 100, 200, 300, 400, 500])
    xt = xtickvalue

    ax.set_xticklabels([xt[0], xt[100], xt[200], xt[300], xt[400], xt[500]])

    ax.set_ylabel('目标数据')
    ax.set_title(figname)
    ax.legend()  # 图例
    ax.grid()  # 网格


def hidtranslation(_hid):
    myhid = _hid
    i = 0
    digit_current_datas = []
    while i <= 100:
        try:
            myhid.readbuffer = []
            result = myhid.write(myhid.writebuffer)
            log.info('send result={}'.format(result))
            sleep(0.002)  # 这里必须等待 使hid数据充分被读到
            if not result:
                log.info('hid write error')
            else:
                digit_current_data = myhid.unpack_read_data(myhid.readbuffer)
                values = digit_current_datas
                log.info('digit current data = {}'.format(digit_current_data))
            i += 1
        except Exception as e:
            log.error('USB hid Error:', e)


hid_name = 'PLC USB HID VER1'
startaddr = 200
datalengh = 10
thishid = hid.MYUSBHID()
thishid.findhiddevice(hid_name)
thishid.start()
log.info('usb hid start')
thishid.updatewritebuffer(startaddr, datalengh)
thishid.setcallback()
currentdatas = []
t1 = threading.Thread(target=hidtranslation, args=(thishid,))  # 线程1指定函数、参数
if thishid.alive:
    t1.setDaemon(True)
    t1.start()
    t1.join()
sleep(3)
thishid.stop()
log.info('usb hid end')

if __name__ == '__main__':
    pass
    
