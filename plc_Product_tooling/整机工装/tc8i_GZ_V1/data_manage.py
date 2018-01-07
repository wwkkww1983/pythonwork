#!/usr/bin/python3
import logging as log
log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


class DataOperation(object):
    def __init__(self):
        ##温度转电压值多项式参数  E=ΣCi*（t90）**i
        self.Etype_J1={0:0,1:50.381187815,2:3.047583693/100,3:-8.568106572/(10**5),
                      4:1.3228195295/(10**7),5:-1.7052958337/(10**10),6:2.0948090697/(10**13),
                       7:-1.2538395/(10**16),8:1.5631726/(10**20)}
        self.Etype_J2={0:2.9645625681*(10**5),1:-1.4976127786*1000,2:3.1787103924,
                       3:-3.1847686701/(10**3),4:1.5720819004/(10**6),5:-3.0691369056/(10**10)}
        self.Etype_K1={0:0,1:39.450128025,2:2.3622373598/100,3:-3.2858906784/(10**4),4:-4.9904828777/(10**6),
                       5:-6.7509059173/(10**8),6:-5.7410327428/(10**10),7:-3.1088872894/(10**12),
                       8:-1.0451609365/(10**14),9:-1.9889266878/(10**17),10:-1.6322697486/(10**20)}
        self.Etype_K2={0:-17.600413686,1:38.921204975,2:1.8558770032/100,3:-9.9457592874/(10**5),
                       4:3.1840945719/(10**7),5:-5.6072844889/(10**10),6:5.6075059059/(10**13),
                       7:-3.2020720003/(10**16),8:9.7151147152/(10**20),9:-1.2104721275/(10**23)}
        self.Etype_Ka={0:118.5976,1:-1.183432/(10**4)}
        pass

    def AD_data_calc(self, data_buffer):
        data_len=len(data_buffer)



    ##寄存器读取电压转换为实际值,参数--寄存器原始值，返回--转换电压(uV)
    def register_volt(self, reg_original_value):
        reg_original_value=reg_original_value-(1<<23)
        reg_original_value=(reg_original_value/(1<<15))*1000
        return reg_original_value

    ##判断8iTC电压是否正常，参数--基准电压类型、读取到的实际电压(mV)，返回值--BOOL
    def judge_source_volt(self, sourcemode, source_volt):
        ##(24V)
        if sourcemode==0:
            if abs(source_volt-24000)<=1500:
                return True
            else:
                log.info('SYS - EP24')
                return 'SYS - EP24'
        ##(±15V)
        elif sourcemode==1:
            if abs(abs(source_volt)-15000)<=1500:
                return True
            else:
                log.info('SYS - EP15')
                return 'SYS - EP15'

        ##(-15V)
        elif sourcemode == 2:
            if abs(abs(source_volt) - 15000) <= 1500:
                return True
            else:
                log.info('SYS - EPM15')
                return 'SYS - EPM15'
        ##(5V)
        elif sourcemode==3:
            if abs(source_volt-5000)<=500:
                return True
            else:
                log.info('SYS - EP5')
                return 'SYS - EP5'
        ##输入参数错误
        else:
            ##log.info
            return False

    ##判断电压值是否在允许误差内，参数--输出类型、AD转换电压、温度转换电压,返回--BOOL
    def judge_volt_validity(self, mode, AD_tran_value, Temp_tran_value):
        ##(-5mV)
        if mode==-5/1000:
            if abs(AD_tran_value-Temp_tran_value)<30:
                return True
            else:
                ##log.info
                return False
        ##(20mV)
        elif mode==20/1000:
            if abs(AD_tran_value-Temp_tran_value)<50:
                return True
            else:
                ##log.info
                return False
        ##(40mV)
        elif mode==40/1000:
            if abs(AD_tran_value-Temp_tran_value)<100:
                return True
            else:
                ##log.info
                return False
        ##(输入参数错误)
        else:
            ##log.info
            return False
            pass




    ##模块冷端温度判断，参数--模拟模块读取的温度值(℃)、8路冷端温度(℃)，返回值--BOOL
    def judge_module_coldside_valid(self, analog_module_readT, coldside_T):
        max_coldside_temp=max(coldside_T)
        min_coldside_temp=min(coldside_T)
        if max_coldside_temp-min_coldside_temp<0.4:
            if abs(analog_module_readT-max_coldside_temp)<0.5 and abs(analog_module_readT-min_coldside_temp)<0.5:
                return True
            else:
                ##log.info
                return False
        else:
            ##log.info
            return False



    ##将温度(单位0.1℃)转换为电压实际值，参数--温度原始值，返回--对应电压(uV)
    def Jtemp2volt(self, temp):
        volt=0
        temp=temp/10.0
        if temp<=760:
            for key in self.Etype_J1:
                volt=volt+self.Etype_J1[key]*(temp**key)
                # print(volt)
        else:
            for key in self.Etype_J2:
                volt=volt+self.Etype_J2[key]*(temp**key)
        return volt

    def Ktemp2volt(self, temp):
        # temp=float(temp)
        e_value=2.718281828459
        t_value=126.9686
        volt=0
        temp=temp/10.0
        if temp<=0:
            for key in self.Etype_K1:
                volt=volt+self.Etype_K1[key]*(temp**key)
        else:
            for key in self.Etype_K2:
                volt=volt+self.Etype_K2[key]*(temp**key)
            volt=volt+self.Etype_Ka[0]*e_value**(self.Etype_Ka[1]*((temp-t_value)**2))

        return volt



if __name__=="__main__":
    do=DataOperation()
    # print(do.register_volt(0x7ff823))
    # print(do.temp2volt(10000))

    for i in range(0,10000,500):
        print("%.1f" %do.Ktemp2volt(i))


