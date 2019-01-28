"""this script parse the content of a xml file"""
from app.communication.operate_port import OperatePort
from utility import crc


class ModbusProtocol():
    """
    modbus协议
    """

    def __init__(self):
        #调用通讯函数
        self.operate_port = OperatePort()

    def __analysis_receive_data(self, receive_data):
        """
        接收数据解析
        :param receive_data:接收到的数据
        :return analysis_data:解析后的数据
        """
        #isinstance（a,b)函数里边有两个参数，
        #如果输入的变量的数据类型和自己定义的数据类型相同，则返回True,否则返回False
        if isinstance(receive_data, list) is not True:
            return []
        data_len = len(receive_data)
        analysis_data = []
        #如果没有接收到数据
        if data_len <= 4:
            pass
        else:
            check_list = receive_data[:-2]
            calculate_crc = crc.add_crc16_check(check_list)[-2:]
            receive_crc = receive_data[-2:]
            #判断CRC校验是否相同
            if calculate_crc == receive_crc:
                if receive_data[1] == 0x03 or receive_data[1] == 0x01:
                    #读命令
                    analysis_data = self.__receive_data_convert(
                        receive_data[3:-2])
                else:
                    #写命令
                    analysis_data = self.__receive_data_convert(
                        receive_data[4:-2])
        return analysis_data

    def __receive_data_convert(self, receive_data):
        """
        对接收的数据进行转换
        :param receive_data  :接收到的数据
        :return analysis_data:解析后的数据
        """
        analysis_data = []
        receive_data_len = len(receive_data)
        if receive_data_len == 1:
            return receive_data
        for i in range(0, receive_data_len - 1, 2):
            convert_data = int(receive_data[i] * 256 + receive_data[i + 1])
            analysis_data.append(convert_data)
        return analysis_data

    def pack_send_data(self, send_code):
        """
        打包发送数据
        :param  send_code:具体的指令码
        :return send data:加CRC校验的数据
        """
        send_data = crc.add_crc16_check(send_code)
        return send_data

    def read_write_data(self, send_data):
        """
        读写数据
        :param  send_data:发送的数据
        :return analysis_receive_data:接收并解析后的数据
        """
        receive_data = self.operate_port.read_write_serial(send_data, 10)
        #print("receive serial data is", receive_data)
        analysis_receive_data = self.__analysis_receive_data(receive_data)
        #print("analysis serial data is", analysis_receive_data)
        return analysis_receive_data
