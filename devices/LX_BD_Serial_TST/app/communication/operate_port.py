"""this script parse the content of a xml file"""
import time
from bsp.device.serial.serial_handle import Ser


class OperatePort():
    """
        接口模块
    """

    def __init__(self):
        """
        指定接口——串口
        """
        self.operate_port = Ser()

    def open_serial(self, serial_name, parity_bit="E", baud_rate=115200):
        """
        打开串口
        :param serial_name:指定要使用的串口
        :return state: True:成功，False：失败
        """
        self.operate_port.close()
        state = self.operate_port.open(serial_name, parity_bit, baud_rate)
        return state

    def close_serial(self):
        """
        关闭串口
        :param :None
        :return:None
        """
        self.operate_port.close()

    def read_write_serial(self, send_data, data_type):
        """
        读写串口数据
        :param  send_data,data_type:发送的数据,选择要接收的数据进制
        :return receive_data:接收的数据
        """
        for i in range(3):
            try:
                if self.operate_port.write(send_data) is True:
                    time.sleep(0.1)
                    receive_data = self.operate_port.read(data_type)
                else:
                    return []
                if receive_data:
                    return receive_data
                if i >= 11:
                    print("超过通讯次数")
            except IOError:
                return []
        return []

    def read_serial(self, data_type):
        """
        读串口数据--16进制数据
        :param  data_type:选择要接收的数据进制
        :return receive_data:接收的数据
        """
        for i in range(10):
            try:
                receive_data = self.operate_port.read(data_type)
                if receive_data:
                    return receive_data
                if i >= 11:
                    print("超过通讯次数")
            except IOError:
                return []
        return []
