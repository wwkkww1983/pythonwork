import pywinusb.hid as hid
import logging as log

log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')

class MYUSBHID(object):
    def __init__(self,name):
        self.name = name
        self.alive = False
        self.device = None
        self.report = None
        self.writebuffer = None
        self.readbuffer = []


    def check_name(self):       # # # # # 返回pc机所有hid设备名
        usb_hid_device_name=[]
        _filter = hid.HidDeviceFilter()
        hid_device = _filter.get_devices()
        for i in hid_device:
            usb_hid_device_name += [i.product_name]
        return usb_hid_device_name

    def start(self):          # # # # # 开始传输
        if self.alive is True:
            pass
        else:
            try:
                _filter = hid.HidDeviceFilter(product_name=self.name)
                hid_device = _filter.get_devices()
                if len(hid_device) > 0:
                    self.device = hid_device[0]
                    self.device.open()
                    self.report = self.device.find_output_reports()
                    self.alive = True
            except Exception as e:
                log.error(e, 'can not open hid device {}'.format(self.name))
            #print(self.report)

    def stop(self):             # # # # 停止传输
        if not self.device:
            pass
        else:
            self.device.close()
            self.alive = False
            log.info('hid device closed:{}'.format(self.device.product_name))

    def setcallback(self):      # # # # 回调函数
        if self.device:
            self.device.set_raw_data_handler(self.read)

    def read(self, rd_report_data):     # # # # 读取数据

        self.readbuffer.append(rd_report_data)
        log.info('received:lengh={}, data={}'.format(len(self.readbuffer), self.readbuffer))
        # return self.readbuffer

    def write(self, wt_report_data):        # # # # 写数据
        result = None
        if len(wt_report_data) < 65 :
            wt_report_data = self.hid_strt_data(wt_report_data)
        if self.device:
            self.readbuffer = []
            result = self.device.send_output_report(wt_report_data)
        return result

    def hid_strt_data(self,fx2n_pack_data):             # # # # 只负责hid协议的打包
        len_hid_data=len(fx2n_pack_data)
        hid_data=[0,len_hid_data,0] + fx2n_pack_data + [0x00 for i in range(62-len_hid_data)]

        return hid_data

    def unpack_hid_data(self):         # # # # 只负责hid协议的解包（传入数据需要list嵌list）
        buffer = self.readbuffer
        newdata = [0 for i in range(3)]
        newlen = 0

        for n in range(len(buffer)):
            newlen += buffer[n][1]
            newdata += buffer[n][3:buffer[n][1] + 3]
        newdata[:3] = [0, newlen, 2]
        log.info('new hid data: total lengh={},data={}'.format(len(newdata), newdata))
        read_len=newdata[1]
        used_data=newdata[3:4+read_len]
        return used_data

if __name__ == "__main__":
    myhid = MYUSBHID('DIGITAL MODULE VER1')
    a = myhid.check_name()
    print(a)