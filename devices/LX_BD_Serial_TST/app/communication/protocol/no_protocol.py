"""this script parse the content of a xml file"""
from app.communication.operate_port import OperatePort


class NoProtocol():
    """
    无协议
    """

    def __init__(self):
        #调用通讯函数
        self.operate_port = OperatePort()

    def read_data(self):
        """
        读数据
        :param  :None
        :return receive_data:接收到的数据
        """
        receive_data = self.operate_port.read_serial(0)
        if receive_data != []:
            receive_data = receive_data.decode('UTF-8', 'ignore')
            #清除掉两侧空格的字符串
            receive_data = receive_data.strip()
            print("解码后的字符串", receive_data)
            return receive_data
        return []
