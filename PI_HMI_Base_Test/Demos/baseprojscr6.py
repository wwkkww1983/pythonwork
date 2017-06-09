# coding:utf8
__author__ = 'admin'

# 写答案以及对答案

from selenium import webdriver
import time
import unittest
# about test case https://en.wikipedia.org/wiki/Test_case
import random
import urllib
import base64
from bs4 import BeautifulSoup
# 用来出来处理html文档，并快速获取网页中各个控件的属性内容的模块 -- fan
# 使用方法介绍 - 博客 http://cuiqingcai.com/1319.html --- 官方文档 - https://www.crummy.com/software/BeautifulSoup/
import re

# 仪表 表格 曲线svg base64 加密，需要使用base64 解密

keyb1000span = ('NODE_1000KY_3', 'NODE_1000KY_5', 'NODE_1000KY_4', 'NODE_1000KY_1', 'NODE_1000KY_10',
                'NODE_1000KY_9', 'NODE_1000KY_6', 'NODE_1000KY_16', 'NODE_1000KY_15', 'NODE_1000KY_11',
                'NODE_1000KY_8', 'NODE_1000KY_14')                      # 0123456789.-
# enter enter del clr esc
keyb1000cont = ('NODE_1000KY_2', 'NODE_1000KY_23', 'NODE_1000KY_7', 'NODE_1000KY_12', 'NODE_1000KY_13')
keyb1000 = ('SPAN_1000STR_24', 'SPAN_1000STR_25', 'SPAN_1000STR_26')    # 最小值id， 最大值id， 输入值id

profilepa = r'C:\Users\admin\AppData\Roaming\Mozilla\Firefox\Profiles\7whknsn0.selenium'    # 自定义profile

ip = '192.168.99.212'
ipp = 'http://'+ip+'/'

profile1 = webdriver.FirefoxProfile(profilepa)
proj = webdriver.Firefox(profile1)
time.sleep(3)
proj.get('http://'+ip+'/')
proj.maximize_window()
proj.implicitly_wait(20)
scr1 = proj.find_element_by_id('NODE_0FS_5')
scr1.click()
time.sleep(3)

class MeterTest(unittest.TestCase):
    def setUp(self):
        pass

    # base64 解码svg数据
    def decode(self, string):
        head = len('data:image/svg+xml;base64,')
        svgfile = string[head:]
        svgg = base64.b64decode(svgfile)
        return svgg

    # 获得仪表的数据，主要是表盘旋转角度，指针旋转角度，刻度显示文本
    def get_meter_info(self, case, part):
        rotate = []     # 获得移动角度
        scale = []      # 获得表盘刻度
        meter = proj.find_element_by_id(part)
        svg = meter.get_attribute('src')
        destring = self.decode(svg)
        soup = BeautifulSoup(destring)
        if case == 1:                             # 计算表盘
            g = soup.find_all('g')
            for i in g:
                if i.attrs == {}:
                    continue
                rotate.append(i.attrs)                    # 获得表盘旋转
            ang = rotate[0]['transform']                  # 把第转换角度转换
            ang = ang.replace('(', 'N')
            ang = ang.replace(' ', 'M')
            result = re.findall(r'(?<=N).*?(?=M)', ang)   # 正则匹配获取的转动角度
            return result[0]                              # 指针旋转角度
        elif case == 2:
            g = soup.find_all('g')
            for i in g:
                if i.attrs == {}:
                    continue
                rotate.append(i.attrs)                    # 获得表盘旋转
            ang = rotate[1]['transform']                  # 把第转换角度转换
            ang = ang.replace('(', 'N')
            ang = ang.replace(' ', 'M')
            result = re.findall(r'(?<=N).*?(?=M)', ang)   # 正则匹配获取的转动角度
            return result[0]                      # 指针旋转角度
        elif case == 3:                           # 获得显示刻度
            text = soup.find_all('text')
            for i in text:
                scale.append(i.get_text())        # 获得表盘刻度数值
            return scale[:-1]
        elif case == 4:
            pass

    # 计算理论指针旋转角度
    def cal_angel(self, inputn, low, hight):
        chge = -135.0 + ((inputn - low) * (270.0 / (hight - low)))      # 转过角度的公式
        ange = str("%.1f" % chge)                                       # 控制1个小数
        return ange

    # 计算刻度显示的文本数值, 有小数点的如数下写
    def calc_scale(self, case, low, hight, kedu):
        resul = []
        if case == 1:
            for i in xrange(0, int(kedu) + 1):
                each = low + i * (hight - low) / kedu
                resul.append(str('%d' % each))
            return resul
        if case == 2:
            for i in xrange(0, int(kedu) + 1):
                each = low + i * (hight - low) / kedu
                resul.append(str('%.3f' % each))
            return resul

    # 测试刻度显示
    def test_custom_scale_text_zero(self):
        self.keytoimput('SPAN_6NUM_3', 0)      # low
        self.keytoimput('SPAN_6NUM_4', 0)      # hight
        scale = self.get_meter_info(3, 'NODE_6MG_1')
        time.sleep(1)
        for i in scale:
            self.assertEqual('0', i)     # 输入0后，刻度都显示0

    # 测试自定义刻度显示下限大于上限
    def test_custom_scale_text_lowlimit_graterthan_hightlimit(self):
        self.keytoimput('SPAN_6NUM_3', 0)      # low
        self.keytoimput('SPAN_6NUM_4', 0)      # hight
        low = random.randint(500, 1000)
        hight = random.randint(200, 450)
        self.keytoimput('SPAN_6NUM_4', hight)       # hight
        self.keytoimput('SPAN_6NUM_3', low)         # low
        scale = self.get_meter_info(3, 'NODE_6MG_1')
        time.sleep(1)
        for i in scale:
            self.assertEqual(str(hight), i)     # 输入0后，刻度都显示0

    # 测试指针旋转，整形
    def test_pointer_to_show_int(self):
        self.keytoimput('SPAN_6NUM_3', 0)      # low
        self.keytoimput('SPAN_6NUM_4', 0)      # hight
        low = random.randint(200, 400)
        hight = random.randint(500,800)
        self.keytoimput('SPAN_6NUM_4', hight)       # hight
        self.keytoimput('SPAN_6NUM_3', low)         # low

        for i in xrange(0, 20):
            inputn = random.randint(100, 1000)
            self.keytoimput('SPAN_6NUM_2', inputn)
            angel = self.get_meter_info(2, 'NODE_6MG_1')
            time.sleep(1)
            if inputn <= low:
                self.assertEqual('-135.0', angel)
            elif inputn >= hight:
                self.assertEqual('135.0', angel)
            else:
                ange = self.cal_angel(inputn, low, hight)
                self.assertEqual(angel, ange)
            time.sleep(1)

    # 测试指针选项，浮点
    def test_pointer_to_show_float(self):
        self.keytoimput('SPAN_6NUM_11', 0)      # low
        self.keytoimput('SPAN_6NUM_12', 0)      # hight
        hight = random.uniform(500, 600)
        hight = float('%0.3f' % hight)      # 需要把值转成3位小数点
        low = random.uniform(200, 400)      # 需要把值转成3位小数点
        low = float('%0.3f' % low)
        self.keytoimput('SPAN_6NUM_12', hight)       # hight
        self.keytoimput('SPAN_6NUM_11', low)         # low
        for i in xrange(0, 20):
            inpu = random.uniform(100, 700)
            inpu = float('%0.3f' % inpu)
            self.keytoimput('SPAN_6NUM_9', inpu)         # input
            ang = self.get_meter_info(2, 'NODE_6MG_10')
            if inpu <= low:
                self.assertEqual('-135.0', ang)
            elif inpu >= hight:
                self.assertEqual('135.0', ang)
            else:
                ange = self.cal_angel(inpu, low, hight)
                self.assertEqual(ang, ange)
            time.sleep(1)

    # 测试自定义刻度显示
    def test_custom_scale_text_int(self):
        self.keytoimput('SPAN_6NUM_3', 0)      # low
        self.keytoimput('SPAN_6NUM_4', 0)      # hight
        for i in xrange(0, 4):
            hight = random.randint(1000, 1500)
            low = random.randint(600, 800)
            self.keytoimput('SPAN_6NUM_4', hight)       # hight
            self.keytoimput('SPAN_6NUM_3', low)         # low
            scale = self.get_meter_info(3, 'NODE_6MG_1')
            res = self.calc_scale(1, low, hight, 5.0)
            self.assertEqual(scale, res)

    # 测试自定义刻度3位小数点，浮点
    def test_custom_scale_text_float(self):
        self.keytoimput('SPAN_6NUM_11', 0)      # low
        self.keytoimput('SPAN_6NUM_12', 0)      # hight
        for i in xrange(0, 20):
            hight = random.uniform(500, 600)
            hight = float('%0.3f' % hight)      # 需要把值转成3位小数点
            low = random.uniform(200, 400)      # 需要把值转成3位小数点
            low = float('%0.3f' % low)
            self.keytoimput('SPAN_6NUM_12', hight)       # hight
            self.keytoimput('SPAN_6NUM_11', low)         # low
            scale = self.get_meter_info(3, 'NODE_6MG_10')
            res = self.calc_scale(2, low, hight, 5.0)
            self.assertEqual(scale, res)

    # 测试表盘旋转
    def test_rotate_the_dials(self):
        angel = self.get_meter_info(1, 'NODE_6MG_13')
        self.assertEqual('90', angel)

    # 把预想的转为输入
    def keytoimput(self, part, num):
        s = proj.find_element_by_id(part)
        s.click()
        time.sleep(0.5)
        ll = []
        string = str(num)
        # 把输入的解析出来
        for i in xrange(0, len(string)):
            elem = string[i]
            if elem in '0123456789':
                proj.find_element_by_id(keyb1000span[int(elem)]).click()
            elif elem == '.':
                proj.find_element_by_id(keyb1000span[-2]).click()
            elif elem == '-':
                proj.find_element_by_id(keyb1000span[-1]).click()
        time.sleep(0.2)
        proj.find_element_by_id(keyb1000cont[0]).click()
        time.sleep(0.8)

    # 随机位数
    def keyinput(self, case):
        if case == 1:
            a1 = random.randint(1, 9)
            proj.find_element_by_id(keyb1000span[a1]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000cont[0]).click()
            time.sleep(0.5)
            value = str(a1)
        elif case == 2:
            a1 = random.randint(1, 9)
            a2 = random.randint(0, 9)
            proj.find_element_by_id(keyb1000span[a1]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000span[a2]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000cont[0]).click()
            time.sleep(0.5)
            value = str(a1) + str(a2)
        elif case == 3:
            a1 = random.randint(1, 9)
            a2 = random.randint(0, 9)
            a3 = random.randint(0, 9)
            proj.find_element_by_id(keyb1000span[a1]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000span[a2]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000span[a3]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000cont[0]).click()
            time.sleep(0.5)
            value = str(a1) + str(a2) + str(a3)
        elif case == 4:
            a1 = random.randint(1, 9)
            a2 = random.randint(0, 9)
            a3 = random.randint(0, 9)
            a4 = random.randint(0, 9)
            proj.find_element_by_id(keyb1000span[a1]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000span[a2]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000span[a3]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000span[a4]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000cont[0]).click()
            time.sleep(0.5)
            value = str(a1) + str(a2) + str(a3) + str(a4)
        elif case == 5:
            a1 = random.randint(1, 6)
            if a1 == 6:                      # 避免出现大于65535的情况
                a2 = random.randint(0, 5)
                a3 = random.randint(0, 5)
                a4 = random.randint(0, 3)
                a5 = random.randint(0, 5)
            else:
                a2 = random.randint(0, 9)
                a3 = random.randint(0, 9)
                a4 = random.randint(0, 9)
                a5 = random.randint(0, 9)
            proj.find_element_by_id(keyb1000span[a1]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000span[a2]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000span[a3]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000span[a4]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000span[a5]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000cont[0]).click()
            time.sleep(0.5)
            value = str(a1) + str(a2) + str(a3) + str(a4) + str(a5)
        return value

    def tearDown(self):
        time.sleep(0.5)


if __name__ == '__main__':
    unittest.main(verbosity=2)
    proj.quit()