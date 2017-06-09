# coding:utf8
__author__ = 'admin'

# 写答案以及对答案

from selenium import webdriver
import time
import unittest
import random
import urllib


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
scr1 = proj.find_element_by_id('NODE_0FS_1')
scr1.click()
time.sleep(1)


class NumberTest(unittest.TestCase):

    # 开始一个测试
    def setUp(self):
        pass

    # 左右标签
    def test_label(self):
        for i in xrange(0, 4):
            num = proj.find_element_by_id('SPAN_2NUM_0')
            vlaue = num.text
            self.assertIn(u'牛', vlaue)
            self.assertIn(u'力=', vlaue)
            time.sleep(0.2)
            a1 = random.randint(1, 9)
            a2 = random.randint(0, 9)
            a3 = random.randint(0, 9)
            num.click()
            time.sleep(0.5)
            proj.find_element_by_id(keyb1000span[a1]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000span[a2]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000span[a3]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000cont[0]).click()
            time.sleep(0.5)
            num = proj.find_element_by_id('SPAN_2NUM_0')
            vlaue = num.text
            string = u'力=' + str(a1) + str(a2) + str(a3) + u'牛'
            self.assertIn(string, vlaue)

        num.click()
        proj.find_element_by_id(keyb1000span[6]).click()
        proj.find_element_by_id(keyb1000span[5]).click()
        proj.find_element_by_id(keyb1000span[5]).click()
        proj.find_element_by_id(keyb1000span[3]).click()
        proj.find_element_by_id(keyb1000span[5]).click()
        proj.find_element_by_id(keyb1000cont[0]).click()
        time.sleep(0.5)
        num = proj.find_element_by_id('SPAN_2NUM_0')
        vlaue = num.text
        self.assertIn(u'力=65535牛', vlaue)

    # 高位补零
    def test_upper_bit_zero(self):
        # # 一位
        # for i in xrange(0, 10):
        #     num.click()
        #     proj.find_element_by_id(keyb1000span[i]).click()
        #     time.sleep(0.2)
        #     proj.find_element_by_id(keyb1000cont[0]).click()
        #     time.sleep(0.5)
        #     value = num.text
        #     string = '0000' + str(i)
        #     self.assertEqual(string, value)
        #     time.sleep(0.2)
        # # 2位
        # for i in xrange(0, 20):
        #     num.click()
        #     time.sleep(0.2)
        #     a1 = random.randint(1, 9)
        #     a2 = random.randint(0, 9)
        #     proj.find_element_by_id(keyb1000span[a1]).click()
        #     time.sleep(0.2)
        #     proj.find_element_by_id(keyb1000span[a2]).click()
        #     time.sleep(0.2)
        #     proj.find_element_by_id(keyb1000cont[0]).click()
        #     time.sleep(0.5)
        #     value = num.text
        #     string = '000' + str(a1) + str(a2)
        #     self.assertEqual(string, value)
        #     time.sleep(0.2)

        # 随机100个数，1~5位
        for i in xrange(0, 5):
            num = proj.find_element_by_id('SPAN_2NUM_3')
            num.click()
            time.sleep(0.5)
            j = random.randint(1, 5)
            if j == 1:
                a1 = random.randint(1, 9)
                proj.find_element_by_id(keyb1000span[a1]).click()
                time.sleep(0.2)
                proj.find_element_by_id(keyb1000cont[0]).click()
                time.sleep(0.5)
                value = num.text
                string = '0000' + str(a1)
                self.assertEqual(string, value)
                time.sleep(0.2)
            elif j == 2:
                a1 = random.randint(1, 9)
                a2 = random.randint(0, 9)
                proj.find_element_by_id(keyb1000span[a1]).click()
                time.sleep(0.2)
                proj.find_element_by_id(keyb1000span[a2]).click()
                time.sleep(0.2)
                proj.find_element_by_id(keyb1000cont[0]).click()
                time.sleep(0.5)
                value = num.text
                string = '000' + str(a1) + str(a2)
            elif j == 3:
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
                value = num.text
                string = '00' + str(a1) + str(a2) + str(a3)
            elif j == 4:
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
                value = num.text
                string = '0' + str(a1) + str(a2) + str(a3) + str(a4)
            elif j == 5:
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
                value = num.text
                string = str(a1) + str(a2) + str(a3) + str(a4) + str(a5)
            self.assertEqual(string, value)
            time.sleep(0.2)

    # 0不显示
    def test_hide_zero(self):
        num = proj.find_element_by_id('NODE_2NUM_4')
        num.click()
        time.sleep(0.2)
        proj.find_element_by_id(keyb1000span[0]).click()   # 输入0
        time.sleep(0.2)
        proj.find_element_by_id(keyb1000cont[0]).click()
        time.sleep(0.5)
        value = proj.find_element_by_id('SPAN_2NUM_4').text
        self.assertEqual('', value)

    # 数据范围
    def test_dynamic_limit(self):

        max = proj.find_element_by_id('SPAN_2NUM_21')
        min = proj.find_element_by_id('SPAN_2NUM_22')
        s = proj.find_element_by_id('SPAN_2NUM_20')

        # max输入
        max.click()
        time.sleep(0.5)
        i = random.randint(1, 3)
        valmax = self.keyinput(i)
        # min输入
        min.click()
        time.sleep(0.5)
        i = random.randint(1, 3)
        valmin = self.keyinput(i)
        # 检查
        s.click()
        time.sleep(0.5)
        maxvalue = proj.find_element_by_id(keyb1000[1]).text
        minvalue = proj.find_element_by_id(keyb1000[0]).text
        self.assertEqual(valmax + '.000', maxvalue)
        self.assertEqual(valmin + '.000', minvalue)
        time.sleep(0.6)
        proj.find_element_by_id(keyb1000cont[-1]).click()

    # 范围颜色
    def test_range_color(self):
        s = proj.find_element_by_id('SPAN_2NUM_25')
        time.sleep(0.2)
        self.keytoimput('SPAN_2NUM_25', 10.201)
        ss = s.get_attribute('style')
        self.assertIn('color: rgb(0, 255, 0)', ss)
        time.sleep(0.5)
        self.keytoimput('SPAN_2NUM_25', 10.200)
        ss = s.get_attribute('style')
        self.assertIn('color: rgb(0, 0, 0)', ss)
        time.sleep(0.5)
        self.keytoimput('SPAN_2NUM_25', 2.555)
        ss = s.get_attribute('style')
        self.assertIn('color: rgb(0, 0, 0)', ss)
        time.sleep(0.5)
        self.keytoimput('SPAN_2NUM_25', 2.554)
        ss = s.get_attribute('style')
        self.assertIn('color: rgb(255, 0, 128)', ss)
        time.sleep(0.5)

    # 自定义范围
    def test_range_color(self):
        maxp = 'SPAN_2NUM_28'
        mixp = 'SPAN_2NUM_27'
        s = 'SPAN_2NUM_29'
        ss = proj.find_element_by_id(s)
        time.sleep(0.2)
        self.keytoimput(maxp, 56.9)
        self.keytoimput(mixp, 20.8)
        # 下限情况
        inn = (10.8, 20.7, 20.8, 0.06, 6.35, 8.45)
        for i in xrange(0, len(inn)):
            self.keytoimput(s, inn[i])
            value = ss.get_attribute('style')
            self.assertIn('color: rgb(255, 0, 128)', value)
            time.sleep(0.5)

        # 中间情况
        inn2 = (20.801, 21.6, 32.5, 56.89, 56.88, 51.2)
        for i in xrange(0, len(inn2)):
            self.keytoimput(s, inn2[i])
            value = ss.get_attribute('style')
            self.assertIn('color: rgb(0, 0, 0)', value)
            time.sleep(0.5)

        # 上限情况
        inn3 = (56.9, 56.901, 57.01, 58.2, 666.3, 999.99)
        for i in xrange(0, len(inn3)):
            self.keytoimput(s, inn3[i])
            value = ss.get_attribute('style')
            self.assertIn('color: rgb(0, 255, 0)', value)
            time.sleep(0.5)

    # 随机键盘输入封装
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

        # 把预想的转为输入

    # 把预想的转为键盘输入
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
        time.sleep(0.5)

    # 结束一个测试
    def tearDown(self):
        time.sleep(0.5)

if __name__ == '__main__':
    unittest.main(verbosity=2)
    proj.quit()