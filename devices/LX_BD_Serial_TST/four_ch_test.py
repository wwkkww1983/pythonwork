"""this script parse the content of a xml file"""
from app.communication.communication import Communication



class FourChannelBD():
    """ Summary of class here...
        四路型BD板
    """

    def __init__(self):
        """
        检测流程初始化
        """
        #设置通讯的串口--修改成电脑上对应的串口
        self.serial_download = "COM32"
        self.communication = Communication()
        self.operate_port = self.communication.modbus_protocal.operate_port
        self.operate_user_port = self.communication.user_protocal.operate_port

    def test_run(self):
        """
        测试运行
        :param :None
        :return:True：成功 False：失败
        """
        #打开通讯串口
        if self.operate_user_port.open_serial(self.serial_download,
                                              "N") is False:
            self.operate_port.close_serial()
            print("usb no connection")
            return False
        #设置循环检测的次数
        for i in range(20):
            print("loop count", i)
            #正确的帧
            bd_type = self.communication.user_pro_get_bd_type()
            print("BD type is ", bd_type)
            """ #漏掉的帧
            miss_frame = self.communication.user_pro_get_bd_type_miss()
            print("miss_frame is ", miss_frame)
            #错误的帧
            error_frame = self.communication.user_pro_get_bd_type_error()
            print("error frame is ", error_frame) """
        return True


if __name__ == '__main__':
    APP = FourChannelBD()
    APP.test_run()
