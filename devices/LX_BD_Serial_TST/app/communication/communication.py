"""this script parse the content of a xml file"""
from app.communication.protocol.modbus_protocol import ModbusProtocol
from app.communication.protocol.no_protocol import NoProtocol
from app.communication.protocol.user_defined_protocol import UserDefinedProtocol


class Communication():
    """ Summary of class here.
        通讯模块
    """

    def __init__(self):
        """
        指定通讯
        """
        #调用MODBUS通讯协议
        self.modbus_protocal = ModbusProtocol()
        #调用无协议
        self.no_protocal = NoProtocol()
        #调用自定义协议
        self.user_protocal = UserDefinedProtocol()

    def user_pro_get_bd_type(self):
        """
        获取BD板的型号
        :param :None
        :return receive_data:返回的数据
        """
        send_code = [0x00, 0x04]
        send_data = self.user_protocal.pack_send_data(send_code)
        receive_data = self.user_protocal.read_write_data(send_data)
        if receive_data == []:
            return []
        return receive_data

    def user_pro_get_bd_type_error(self):
        """
        获取BD板的型号
        :param :None
        :return receive_data:返回的数据
        """
        send_code = [0x00, 0x07]
        send_data = self.user_protocal.pack_send_data(send_code)
        send_data.append(0x66)
        receive_data = self.user_protocal.read_write_data(send_data)
        if receive_data == []:
            return []
        return receive_data

    def user_pro_get_bd_type_miss(self):
        """
        获取BD板的型号
        :param :None
        :return receive_data:返回的数据
        """
        send_code = [0x00, 0x04]
        #send_data = self.user_protocal.pack_send_data(send_code)
        receive_data = self.user_protocal.read_write_data(send_code)
        if receive_data == []:
            return []
        return receive_data

    def user_pro_read_bd_ch_data(self):
        """
        读db板的通道值
        :param :None
        :return receive_data:返回的数据
        """
        send_code = [0x02, 0x06, 0x01, 0x04]
        send_data = self.user_protocal.pack_send_data_crc(send_code)
        receive_data = self.user_protocal.read_write_data_crc(send_data)
        if receive_data == []:
            return []
        return receive_data

    def user_pro_write_bd_ch_data(self, ch_num, data_hight, data_low):
        """
        写BD板通道值
        :param ch_num, data_hight, data_low:通道号,数据高位,数据低位
        :return :True 和 False
        """
        send_code = [0x03, 0x08, ch_num, 0x01, data_hight, data_low]
        send_data = self.user_protocal.pack_send_data_crc(send_code)
        receive_data = self.user_protocal.read_write_data_crc(send_data)
        if receive_data == []:
            return False
        if receive_data[0] == 0x06:
            return True
        return False


if __name__ == '__main__':
    pass
