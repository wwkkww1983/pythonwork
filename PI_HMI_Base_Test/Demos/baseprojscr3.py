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
scr1 = proj.find_element_by_id('NODE_0FS_2')
scr1.click()
time.sleep(1)


class WordSwitchTest(unittest.TestCase):

    # 开始一个测试
    def setUp(self):
        pass

    # 值设置
    def test_setvalue(self):
        proj.find_element_by_id('NODE_3WS_0').click()
        time.sleep(0.5)
        des = proj.find_element_by_id('SPAN_3NUM_5')
        self.assertEqual('-50', des.text)

    # 32位的高地址fang反转
    def test_hight_low_exchange(self):
        proj.find_element_by_id('NODE_3WS_0').click()
        time.sleep(0.5)
        des = proj.find_element_by_id('SPAN_3NUM_5')
        self.assertEqual('-50', des.text)
        time.sleep(0.5)
        s1 = proj.find_element_by_id('SPAN_3NUM_3')
        self.assertEqual('FFFFFFCE', s1.text)
        time.sleep(0.5)
        proj.find_element_by_id('NODE_3WS_4').click()
        time.sleep(0.8)
        self.assertEqual('FFCEFFFF', s1.text)

    # 自加5
    def test_incvalue5(self):
        bef = proj.find_element_by_id('SPAN_3NUM_9')
        befv = int(bef.text)
        for i in xrange(0, 20):
            proj.find_element_by_id('NODE_3WS_8').click()
            time.sleep(0.5)
            val = int(bef.text)
            if (befv + 5) <= 80:
                self.assertEqual(5, (val - befv))
                befv = val
            else:
                self.assertEqual(int(bef.text), befv)

    # 自加5 终点返回-2
    def test_incvalue5return2(self):
        bef = proj.find_element_by_id('SPAN_3NUM_10')
        befv = int(bef.text)
        for i in xrange(0, 20):
            proj.find_element_by_id('NODE_3WS_11').click()
            time.sleep(0.5)
            val = int(bef.text)
            if (befv + 5) <= 40:
                self.assertEqual(5, (val - befv))
            else:
                self.assertEqual('-2', bef.text)
            befv = val

    # 递加-6
    def test_decvalue6(self):
        bef = proj.find_element_by_id('SPAN_3NUM_17')
        befv = int(bef.text)
        for i in xrange(0, 20):
            proj.find_element_by_id('NODE_3WS_14').click()
            time.sleep(0.5)
            val = int(bef.text)
            if (befv + (-6)) >= -22:
                self.assertEqual(6, (befv - val))
                befv = val
            else:
                self.assertEqual(int(bef.text), befv)

    # 递减-6终点返回-3
    def test_decvalue6return3(self):
        bef = proj.find_element_by_id('SPAN_3NUM_16')
        befv = int(bef.text)
        for i in xrange(0, 20):
            proj.find_element_by_id('NODE_3WS_15').click()
            time.sleep(0.5)
            val = int(bef.text)
            if (befv + (-5)) >= -22:
                self.assertEqual(6, (befv - val))
            else:
                self.assertEqual('-3', bef.text)
            befv = val

    # 自动变化
    def test_autochange(self):
        bef = proj.find_element_by_id('SPAN_3NUM_27')
        img = proj.find_element_by_id('NODE_3WL_20')
        self.keytoimput('SPAN_3NUM_27', 0)
        first = 0
        for i in xrange(0, 20):
            befv = int(bef.text)
            if i > 0:
                self.assertEqual(1, abs(befv - first))
            first = befv
            value = img.get_attribute('src')
            if (i < 31) and (i != 0):
                imm = '000' + str(i + 10) + '.png'
                self.assertIn(imm, value)
            time.sleep(2)

    # 手动变化递加
    def test_manualchangeinc(self):
        bef = proj.find_element_by_id('SPAN_3NUM_28')
        img = proj.find_element_by_id('NODE_3WL_21')
        self.keytoimput('SPAN_3NUM_28', 0)
        value = img.get_attribute('src')
        self.assertEqual(ipp + 'img/00009.png', value)
        for i in xrange(0, 31):
            img.click()
            time.sleep(0.5)
            self.assertEqual((i + 1), int(bef.text))
            im = '000' + str(i + 10) + '.png'
            value = img.get_attribute('src')
            self.assertIn(im, value)

    # 手动变化递减
    def test_manualchangedec(self):
        bef = proj.find_element_by_id('SPAN_3NUM_29')
        img = proj.find_element_by_id('NODE_3WL_25')
        self.keytoimput('SPAN_3NUM_29', 31)
        value = img.get_attribute('src')
        self.assertEqual(ipp + 'img/00040.png', value)
        for i in xrange(0, 31):
            img.click()
            time.sleep(0.5)
            self.assertEqual((30 - i), int(bef.text))
            im = '000' + str(39 - i) + '.png'
            value = img.get_attribute('src')
            self.assertIn(im, value)

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

    #  结束一次测试
    def tearDown(self):
        time.sleep(1)

if __name__ == '__main__':
    unittest.main(verbosity=2)
    proj.quit()