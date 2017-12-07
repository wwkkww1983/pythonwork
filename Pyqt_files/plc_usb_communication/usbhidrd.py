# !/usr/bin/env python3
# -*- coding: utf-8 -*-

import pywinusb.hid as hid
from time import ctime, sleep
import logging as log
import threading
from crccheck.checksum import Checksum8
log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


class MYUSBHID(object):
    def __init__(self):
        self.name = ''
        self.alive = False
        self.device = None
        self.report = None
        self.writebuffer = []
        self.writeresult = False
        self.readbuffer = []
        self.readbuffermaxlen = 0

    def nosuchdevicerror(self, errorinfo):
        log.error(errorinfo, ' -- no such device error: hid{0}, device{1}'.format(self.name, self.device))

    def notaliverror(self, errorinfo):
        log.error(errorinfo, ' -- device not alive error: hid{0}, device{1}, alive{2}'.format(
            self.name, self.device, self.alive))

    def findhiddevice(self, name):
        self.name = name
        try:
            _filter = hid.HidDeviceFilter(product_name=self.name)
            hid_device = _filter.get_devices()
            if len(hid_device) > 0:
                self.device = hid_device[0]
                log.info('find hid device: {0}(pid={1}, vid={2})'.format(self.name, self.device.product_id,
                                                                         self.device.vendor_id))
        except Exception as e:
            log.error(e, 'find hid device fail: {}'.format(self.name))

    def start(self):
        if self.device:
            if not self.alive:
                try:
                    self.device.open()
                    self.alive = True
                except Exception as e:
                    self.notaliverror('start,open')
            else:
                log.info('hid device has been started: {}'.format(self.name))
        else:
            self.nosuchdevicerror('start')

    def stop(self):
        if self.device:
            if self.alive:
                self.device.close()
                self.alive = False
            else:
                log.info('hid device has been stopped: {}'.format(self.name))
        else:
            self.nosuchdevicerror('stop')

    def updatewritebuffer(self, operal, startadd, lengh, data):
        if self.name == 'DIGITAL MODULE VER1':
            operal = 'read'
            data = None
        if self.name == 'ANALOG MODULE VER1':
            operal = 'read'
            data = None
        if self.name == 'PLC USB HID VER1':
            pass
        write_data = self.pack_write_data(operal, startadd, lengh, data)
        l = len(list(write_data))
        wtbffr = [0x00 for i in range(65)]
        if operal == 'read':
            wtbffr[:16] = [0, 0xd, 0] + list(write_data)
        if operal == 'write':
            wtbffr[:(l+2)] = [0x11, 0] + list(write_data)
            # wtbffr[:(l + 2)]=[0x11, 0]+[2, 63, 49, 48, 52, 48, 48, 48, 48, 50, 59, 64, 49, 51, 3, 60, 59]
        log.info('lengh={}, send list: {}'.format(len(wtbffr), wtbffr))
        sleep(.1)
        self.writebuffer = wtbffr

    def setcallback(self):
        if self.device:
            self.device.set_raw_data_handler(self.read)
        else:
            self.nosuchdevicerror('setcallback')

    def read(self, rd_report_data):
        self.readbuffer.append(rd_report_data)
        if len(self.readbuffer) == self.readbuffermaxlen:
            log.info('received:lengh={}, data={}'.format(len(self.readbuffer), self.readbuffer))
            return self.readbuffer

    def write(self, wt_report_data):
        self.writeresult = False
        if self.device:
            self.writeresult = self.device.send_output_report(wt_report_data)
        else:
            self.nosuchdevicerror('write')
        return self.writeresult

    def pack_write_data(self, operal_type='read', start_address=0, operal_word_lengh=1, wt_data=None):
        """
        将数据组装为串口数据形式
        :param start_address: D0偏移字（内部计算转换成字节数），字
        :param operal_word_lengh: read/write数据长度，字
        :param wt_data: 读取或写入数据，字节 写入用
        :param operal_type: 操作类型：read/write
        :return: 待传输字节串
        """
        if operal_type == 'read':
            # 根据读长度要对usb_hid读缓存readbuffer进行区分1~14word, 1条帧；15~30word,2条帧；31、32word,3条帧
            self.readbuffermaxlen = ((operal_word_lengh + 1) * 4 - 1) // 62 + 1
        if operal_type == 'write':
            self.readbuffermaxlen = 1

        stx = [0x02]
        etx = [0x03]
        # 起始标识，结束标识

        func_code = {'read': [0x45, 0x30, 0x30], 'write': [0x45, 0x31, 0x30]}[operal_type]
        # 读写功能码，3 bytes

        def pack_strt_addr(strt_addr_):
            # 读写起始地址，4_bytes list
            d0_fmt = 0x4000
            d8000_fmt = 0x0E00
            strt_addr_str = ''
            if strt_addr_ in range(0, 8000):
                strt_addr_str = '{:#06X}'.format(strt_addr_ * 2 + d0_fmt)
            elif strt_addr_ in range(8000, 8255):
                strt_addr_str = '{:#06X}'.format((strt_addr_ - 8000) * 2 + d8000_fmt)
            strt_addr_fmt = [ord(letter) for letter in strt_addr_str][2:]
            return strt_addr_fmt
        start_address_code = pack_strt_addr(start_address)

        def pack_lengh(len_):
            lengh = []
            # 读写长度 2_bytes list,注意A~F必须是大写的，否则会出错
            if operal_word_lengh in range(1, 33):
                len_str = '{:#04X}'.format(operal_word_lengh * 2)
                lengh = [ord(letter) for letter in len_str][2:]
            return lengh
        lengh_code = pack_lengh(operal_word_lengh)

        # 写指令时的数据（列表类型）组装
        wt_data_code = []
        if operal_type == 'read':
            pass
        if operal_type == 'write':
            def pack_wtdata(nums):
                wt_codes = []
                for x in nums:
                    h = 0
                    b = int(x).to_bytes(2, byteorder='little', signed=True)
                    l = h.from_bytes(b, 'big', signed=False)
                    h_str = '{0:#06X}'.format(l)
                    wt_codes += [ord(letter) for letter in h_str[2:]]
                return wt_codes
            wt_data_code = pack_wtdata(wt_data)

        def pack_check_sum(func_code_, strt_addr_code_, len_code_, wt_data_code_, etx_):
            checksum = []
            # 校验和，1 bytes。功能码、起始地址、数据和结束标识参与校验，起始标识不校验
            check = Checksum8()
            if lengh_code:
                chencksum = []
                if operal_type == 'read':
                    checksum_int = check.calc(func_code_ + strt_addr_code_ + len_code_ + etx_)
                    checksum_str = '{:#04X}'.format(checksum_int)
                    checksum = [ord(letter) for letter in checksum_str][2:]
                elif operal_type == 'write' and wt_data_code_:
                    checksum_int = check.calc(func_code_ + strt_addr_code_ + len_code_ + wt_data_code_ + etx_)
                    checksum_str = '{:#04X}'.format(checksum_int)
                    checksum = [ord(letter) for letter in checksum_str][2:]
                else:
                    log.error('chencksum error')
                return checksum
        checksum_code = pack_check_sum(func_code, start_address_code, lengh_code,  wt_data_code, etx)

        log.info("""
        "the follow parameter packed:"
            "stx: {0}: "
            "function code: {1}; "
            "start address: {2}; "
            "data lengh: {3};"
            "write data: {4}; "
            "etx: {5}; "
            "check sum: {6}""".format(
            stx, func_code, start_address_code, lengh_code, wt_data_code, etx, checksum_code))
        # 待发送数据list
        _data_list = []
        if operal_type == 'read':
            _data_list = stx + func_code + start_address_code + lengh_code + etx + checksum_code
        elif operal_type == 'write':
            _data_list = stx + func_code + start_address_code + lengh_code + wt_data_code + etx + checksum_code
        return _data_list

    # @staticmethod
    def unpack_read_data(self, read_buffer):
        """
        从hid回调数据中获取有效数据并解析。
        :param read_buffer: 数字板：64，模拟板：32
        :return: 解析后的数字板或模拟板寄存器数据
        """
        if read_buffer[0][0]== 1:
            return read_buffer
        if read_buffer[0][0] == 0:
            buffer = read_buffer
            newdata = [0 for i in range(3)]
            newlen = 0

            # hid读回数据处理 ： 00
            for n in range(len(buffer)):
                newlen += buffer[n][1]
                newdata += buffer[n][3:buffer[n][1] + 3]
            newdata[:3] = [0, newlen, 2]
            log.info('new hid data: total lengh={},data={}'.format(len(newdata), newdata))

            used_data = newdata[4:-3]
            data_chr_list = [chr(i) for i in used_data]
            log.info('lengh={0}, data_chr_list={1}'.format(len(data_chr_list), data_chr_list))
            data_int_list = []
            unpack_lengh = len(data_chr_list)
            for s in range(0, unpack_lengh, 4):
                if 0 <= s <= unpack_lengh - 4:
                    a = data_chr_list[s + 2] + data_chr_list[s + 3] + data_chr_list[s] + data_chr_list[s + 1]
                    data_int_list.append(int(a, 16))
                else:
                    pass
            log.info('data int list={}'.format(data_int_list))
            unpacked_data = data_int_list
            return unpacked_data


if __name__ == '__main__':
    def hidtranslation(_hid):
        myhid = _hid
        i = 0
        while i <= 100:
            try:
                myhid.readbuffer = []
                result = myhid.write(myhid.writebuffer)
                log.info('send result={}'.format(result))
                sleep(0.02)  # 这里必须等待 使hid数据充分被读到
                if not result:
                    log.info('hid write error')
                else:
                    digit_current_data = myhid.unpack_read_data(myhid.readbuffer)
                    log.info('digit current data ={}'.format(digit_current_data))
                i += 1
            except Exception as e:
                log.error('USB hid Error:', e)

    # hid_name = 'DIGITAL MODULE VER1'
    # hid_name = 'ANALOG MODULE VER1'
    hid_name = 'PLC USB HID VER1'
    # operaltype = 'read'
    # startaddr = 0
    # datalengh = 32

    operaltype = 'read'
    startaddr = 8000
    data = None
    datalengh = 1

    thishid = MYUSBHID()
    thishid.findhiddevice(hid_name)
    thishid.start()
    log.info('usb hid start')
    thishid.updatewritebuffer(operaltype, startaddr, datalengh, data)
    thishid.setcallback()

    t1 = threading.Thread(target=hidtranslation, args=(thishid,))  # 线程1指定函数、参数
    if thishid.alive:
        t1.setDaemon(True)
        t1.start()
        t1.join()

    sleep(3)
    thishid.stop()
    log.info('usb hid end')

