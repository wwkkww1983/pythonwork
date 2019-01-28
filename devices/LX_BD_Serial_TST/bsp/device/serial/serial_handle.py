# coding:utf-8
"""this script parse the content of a xml file"""
import serial
import serial.tools.list_ports


class Stm32BLException(Exception):
    """General STM32 loader exception"""


class SerialException(Stm32BLException):
    """Serial communication Exception"""


class Ser():
    """ Summary of class here.
    串口类
    """

    def __init__(self):
        """
        串口初始化
        """
        self.is_opened = False
        self.serial_port = None

    def open(self,
             serial_name,
             parity_bit='E',
             baud_rate=115200,
             byte_size=8,
             stop_bits=1):
        """
        打开串口
        :param :略
        :return:True:成功，False：失败
        """
        try:
            self.serial_port = serial.Serial(
                port=serial_name,
                baudrate=baud_rate,
                bytesize=byte_size,
                parity=parity_bit,
                stopbits=stop_bits,
                timeout=0.1)
            self.is_opened = True
            return True
        except (IOError, ValueError):
            return False

    def close(self):
        """
        关闭串口
        :param :None
        :return:None
        """
        if self.is_opened is True:
            self.serial_port.close()
            self.is_opened = False

    def write(self, data):
        """
        写数据到串口
        :param data:数据
        :return:True:成功，False：失败
        """
        if self.is_opened is True:
            self.serial_port.write(bytes(data))
            return True
        return False

    def read(self, data_type=10):
        """
        读串口所有数据--16进制字符串转成10进制列表
        :param data_type:根据需要选择数据类型
        :return response:读到的数据
        """
        response = []
        if self.is_opened is True:
            response = self.serial_port.readall()
            if data_type == 10:
                response = convert_to_decimal(response)
        return response

    def search(self):
        """
        搜索串口设备
        :param :None
        :return serial_name:串口名
        """
        plist = list(serial.tools.list_ports.comports())
        plist_len = len(plist)
        serial_name = []
        if plist_len > 0:
            for i in range(plist_len):
                plist_0 = list(plist[i])
                serial_name.append(plist_0)
        return serial_name


def convert_to_decimal(string):
    """
    16进制字符串转换成10进制列表
    :param string:要转换的字符串
    :return result:转换结果
    """
    res = []
    result = []
    for item in string:
        res.append(item)
    for i in res:
        result.append(int(i))
    return result
