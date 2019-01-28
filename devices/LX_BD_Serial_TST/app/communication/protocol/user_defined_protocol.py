"""this script parse the content of a xml file"""
from app.communication.operate_port import OperatePort
from utility import crc


class UserDefinedProtocol():
    """
    自定义协议
    """

    def __init__(self):
        #调用通讯函数
        self.operate_port = OperatePort()

    def __analysis_receive_data(self, receive_data):
        """
        自定义协议接收数据解析
        :param receive_data:接收到的数据
        :return user_analysis_data:解析后的数据
        """
        if isinstance(receive_data, list) is not True:
            return []
        data_len = len(receive_data)
        user_analysis_data = []
        #如果没有接收到数据
        if data_len == 0:
            pass
        elif data_len == 1:
            user_analysis_data = receive_data
        else:
            check_list = receive_data[:-2]
            user_calculate_crc = crc.add_crc16_check(check_list)[-2:]
            receive_crc = receive_data[-2:]
            #判断自定义协议CRC校验是否相同
            if user_calculate_crc == receive_crc:
                if receive_data[0] == 0x00 or receive_data[0] == 0x06:
                    user_analysis_data = self.__receive_data_convert(
                        receive_data[2:-2])
                else:
                    user_analysis_data = self.__receive_data_convert(
                        receive_data[4:-2])
        return user_analysis_data

    def read_write_data(self, send_data):
        """
        自定义协议读写数据
        :param  send_data:发送的数据
        :return analysis_receive_data:接收并解析后的数据
        """
        user_receive_data = self.operate_port.read_write_serial(send_data, 10)
        #print("自定义协议接收到的数据", user_receive_data)
        analysis_receive_data = self.__analysis_receive_data(user_receive_data)
        #print("自定义协议解析后的数据", analysis_receive_data)
        return analysis_receive_data

    def pack_send_data(self, send_code):
        """
        自定义协议打包发送数据
        :param  send_code:具体的指令码
        :return user_send_data:加CRC校验的数据
        """
        user_send_data = crc.add_crc16_check(send_code)
        return user_send_data

    def __receive_data_convert(self, receive_data):
        """
        自定义协议对接收的数据进行转换
        :param receive_data  :接收到的数据
        :return user_analysis_data:解析后的数据
        """
        user_analysis_data = []
        user_receive_data_len = len(receive_data)
        if user_receive_data_len == 1:
            return receive_data
        for i in range(0, user_receive_data_len - 1, 2):
            convert_data = int(receive_data[i] * 256 + receive_data[i + 1])
            #对负数的情况进行处理
            if convert_data > 0x7FFF:
                convert_data = convert_data - 0xFFFF
            user_analysis_data.append(convert_data)
        return user_analysis_data
