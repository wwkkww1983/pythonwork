#! /usr/bin/env python
# -*- coding: utf-8 -*-

'''
win下使用的HID设备通讯帮助类
'''
__author__ = "jakey.chen"
__version__ = "v1.0"
import threading
from fx2n import FX2N

import pywinusb.hid as hid

class hidHelper(object):

    def __init__(self, vid=0x1391, pid=0x2111):
        self.alive = False
        self.device = None
        self.report = None
        self.vid = vid
        self.pid = pid
        self.name = 'PLC USB HID VER1'
        self.readbuff =[]

    def start(self):
        '''
        开始，打开HID设备
        '''
        _filter = hid.HidDeviceFilter(product_name=self.name)
        hid_device = _filter.get_devices()
        if len(hid_device) > 0:
            self.device = hid_device[0]
            self.device.open()
            self.report = self.device.find_output_reports()
            self.alive  = True


    def stop(self):
        '''
        停止，关闭HID设备
        '''
        self.alive = False
        if self.device:
            self.device.close()

    def setcallback(self):
        '''
        设置接收数据回调函数
        '''
        if self.device:
            self.device.set_raw_data_handler(self.read)

    def read(self, data):
        '''
        接收数据回调函数
        '''
        self.readbuff.append(data)
        print(data)
        print([hex(item).upper() for item in data[1:]])
        # print('end')

    # def write(self, send_list):
    #     '''
    #     向HID设备发送数据
    #     原demo定义的函数
    #     '''
    #     if self.device:
    #         if self.report:
    #             self.report[0].set_raw_data(send_list)
    #             bytes_num = self.report[0].send()
    #             return bytes_num
    def write(self, send_list):
        '''
        向设备发送数据
        PLC USB HID协议专用
        '''

        if self.device:
            if self.report:
                self.readbuff = []
                self.device.send_output_report(send_list)
                return 65
    def data_handle_test(self,read_buffer,mod =0):
        buffer = read_buffer
        newdata = [0 for i in range(3)]
        newlen = 0

        # hid读回数据处理 ： 00
        for n in range(len(buffer)):
            newlen += buffer[n][1]
            newdata += buffer[n][3:buffer[n][1] + 3]
        newdata[:3] = [0, newlen, 2]
        # log.info('new hid data: total lengh={},data={}'.format(len(newdata), newdata))

        used_data = newdata[4:-3]
        data_chr_list = [chr(i) for i in used_data]
        print(data_chr_list)
        # log.info('data_chr_list={}'.format(data_chr_list))
        data_int_list = []
        if mod ==1:
           unpacked_data = data_chr_list

        else:
            unpack_lengh = len(data_chr_list)
            for s in range(unpack_lengh):
                if -1 < s < 128:
                    if s % 4 == 0:
                        temp_data = data_chr_list[s + 2] + data_chr_list[s + 3] + data_chr_list[s] + \
                                    data_chr_list[s + 1]
                        print(int(data_chr_list[s+2], 16))
                        if int(data_chr_list[s+2], 16) < 8:
                            data_int_list.append(int(temp_data, 16))
                        else:
                            temp_data = int(temp_data, 16)
                            temp_data = -((temp_data ^ 0xffff) + 1)
                            data_int_list.append(temp_data)
                    else:
                        pass

            # log.info('data int list={}'.format(data_int_list))
            unpacked_data = data_int_list
        return unpacked_data
if __name__ == '__main__':
    import time
    # def write():
    #     if myhid.alive:
    #         myhid.setcallback()
    #         send_list = [0, 13, 0, 2, 69, 48, 48, 52, 48, 48, 50, 48, 50, 3, 68, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                      0, 0, 0, 0, 0]
    #         myhid.write(send_list)
    #         time.sleep(0.5)
    #         print(myhid.buff)
    #         print('2')
    #
    # def write2():
    #     if myhid.alive:
    #         myhid.setcallback()
    #         send_list = [0, 13, 0, 2, 69, 48, 48, 52, 48, 48, 52, 48, 50, 3, 68, 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    #         myhid.write(send_list)
    #         time.sleep(0.5)
    #
    #         print(myhid.buff)
    #         print('aaa')
    #         time.sleep(0.5)

    error_str = ''
    error_list = [2,6,5,9,8]
    for i in range(len(error_list)):
        error_str = error_str + str(error_list[i]) + '、'
    error_str = '端子' + error_str + '连接在一起'

    print(error_str)












    myhid = hidHelper()
    myfx2n = FX2N()
    myhid.start()


    # if myhid.alive:
    #     myhid.setcallback()
    #     # myhid.write([0, 13, 0, 2, 69, 48, 48, 52, 48, 48, 52, 48, 50, 3, 65, 48, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    #
    #     send_list = []
    #     # send_list = myfx2n.pack_writefun_data(3, 1, [2,0])
    #     send_list = myfx2n.read_extended_module_directive_pack(0,19, 1)
    #     # send_list = [0, 0x11, 0] + list(send_list) + [0x00 for i in range(48)]
    #     # send_list = [2,69, 55,56, 56, 48, 49, 3,53, 48]
    #     a = len(send_list)
    #     print(a)
    #     send_list = [0, 0xd, 0] + list(send_list) + [0x00 for i in range(49)]
    #
    #     print('send list', send_list)
    #     myhid.write(send_list)
    #     time.sleep(0.005)
    #
    #     c = myhid.data_handle_test(myhid.readbuff)
    #     print(c)
    #
    #     f =0x40f6
    #
    #     n = -((f ^ 0xffff)+1)
    #     print(n)
    #
    #     n = ((-n)^0xffff)+1
    #     print(n)
    #     print(f)
    #     # d=32333
    #     # d = int(d)
    #     # d = hex(d)[2:]
    #     # #
    #     # # d = '{:#02X}'.format(d)
    #     #
    #     # d = d.zfill(4)
    #     # print(d)
    #     # dDes_high = int(d[:2],16)
    #     # dDes_low = int(d[2:],16)
    #     # print(dDes_high)
    #     # print(dDes_low)
    #     # print(d)
    #     # send_list = myfx2n.read_extended_module_directive_pack(0,20, 1)
    #     # send_list = [0, 0xd, 0] + list(send_list) + [0x00 for i in range(49)]
    #     #
    #     # print('send list', send_list)
    #     # myhid.write(send_list)
    #     # time.sleep(0.005)
    #     #
    #     # d = myhid.data_handle_test(myhid.readbuff)
    #     # print(d)
    #     #
    #     # code_temperature = c+d
    #     # code_temp_list= []
    #     #
    #     # high16_data = hex(code_temperature[0])[2:]
    #     # high16_data = high16_data + '0' * (4 - len(high16_data))
    #     # low16_data = hex(code_temperature[1])[2:]
    #     #
    #     # code_temperature = high16_data + low16_data
    #     # print(code_temperature)
    #     # code_temp_list.append(int(code_temperature, 16))
    #
    #
    #     # print(code_temp_list)
    #
    #     # n=[65526,15]
    #     # m=
    #     # #
    #     # # a = hex(n[0])[2:] + hex(n[1])[2:]
    #     # # print(a)
    #     # # m.append(int(a, 16))
    #     #
    #     #
    #     #
    #     # print(m)
    #     # a = myfx2n.protocol_data_analysis([21])
    #     # print(a)
    #
    # # t1 = threading.Thread(target=write, args=())
    # # t2 = threading.Thread(target=write2, args=())
    # # a=[t1, t2]
    # # for t in a:
    # #     print(t)
    # #     t.start()
    # #     t.join()

