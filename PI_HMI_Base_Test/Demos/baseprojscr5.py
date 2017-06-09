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
scr1 = proj.find_element_by_id('NODE_0FS_4')
scr1.click()
time.sleep(3)

class CombinationTest(unittest.TestCase):
    def setUp(self):
        pass

    # 组合开关位置off
    def test_bit_set_off(self):
        off = proj.find_element_by_id('NODE_5CmpFS_4')
        off.click()
        time.sleep(0.5)
        off.click()
        chelist = ('NODE_5BS_6', 'NODE_5BS_7', 'NODE_5BS_8')
        for ele in chelist:
            el = proj.find_element_by_id(ele)
            ss = el.get_attribute('src')
            self.assertEqual(ipp + 'img/00004.png', ss)

    # 组合开关位置on
    def test_bit_set_on(self):
        on = proj.find_element_by_id('NODE_5CmpFS_3')
        on.click()
        time.sleep(0.5)
        on.click()
        chelist = ('NODE_5BS_6', 'NODE_5BS_7', 'NODE_5BS_8')
        for ele in chelist:
            el = proj.find_element_by_id(ele)
            ss = el.get_attribute('src')
            self.assertEqual(ipp + 'img/00005.png', ss)

    # 位复制
    def test_bit_copy(self):
        mlist = ('NODE_5BS_6', 'NODE_5BS_7', 'NODE_5BS_8')
        ylist = ('NODE_5BS_28', 'NODE_5BS_29', 'NODE_5BS_30')
        copy = proj.find_element_by_id('NODE_5CmpFS_1')

        # 把相同的变不同
        for mele, yele in zip(mlist, ylist):
            mel = proj.find_element_by_id(mele)
            mss = mel.get_attribute('src')
            yel = proj.find_element_by_id(yele)
            yss = yel.get_attribute('src')
            if mss == yss:
                proj.find_element_by_id(yele).click()
                time.sleep(0.5)
        copy.click()
        time.sleep(0.5)

        for mele, yele in zip(mlist, ylist):
            mel = proj.find_element_by_id(mele)
            mss = mel.get_attribute('src')
            yel = proj.find_element_by_id(yele)
            yss = yel.get_attribute('src')
            self.assertEqual(yss, mss)

    # 字设置55
    def test_num_setvalue(self):
        alist = ('SPAN_5NUM_12', 'SPAN_5NUM_13', 'SPAN_5NUM_14', 'SPAN_5NUM_15', 'SPAN_5NUM_16')
        for ele in alist:
            self.keytoimput(ele, 0)
        proj.find_element_by_id('NODE_5CmpFS_24').click()
        time.sleep(1)
        for ele in alist:
            a = proj.find_element_by_id(ele)
            self.assertEqual('55.00', a.text)

    # 字复制hdw到d70
    def test_num_copy(self):
        alist = ('SPAN_5NUM_12', 'SPAN_5NUM_13', 'SPAN_5NUM_14', 'SPAN_5NUM_15', 'SPAN_5NUM_16')
        blist = ('SPAN_5NUM_17', 'SPAN_5NUM_18', 'SPAN_5NUM_19', 'SPAN_5NUM_20', 'SPAN_5NUM_21')
        copy = proj.find_element_by_id('NODE_5CmpFS_10')

        for mele, yele in zip(alist, blist):
            mel = proj.find_element_by_id(mele)
            mss = mel.text
            yel = proj.find_element_by_id(yele)
            yss = yel.text
            if mss == yss or (yss == '0.00'):
                self.keytoimput(yele, random.randint(100, 200))
        copy.click()
        time.sleep(0.5)

        for mele, yele in zip(alist, blist):
            mel = proj.find_element_by_id(mele)
            mss = mel.text
            yel = proj.find_element_by_id(yele)
            yss = yel.text
            self.assertEqual(yss, mss)

    # 字递加55 上限500
    def test_num_inc(self):
        alist = ('SPAN_5NUM_12', 'SPAN_5NUM_13', 'SPAN_5NUM_14', 'SPAN_5NUM_15', 'SPAN_5NUM_16')
        inc = proj.find_element_by_id('NODE_5CmpFS_25')
        firslist = []

        # 随机设置初始值
        for ele in alist:
            a = random.randint(10, 100)
            firslist.append(a)
            self.keytoimput(ele, a)
        # 执行13次点击
        for i in xrange(0, 13):
            inc.click()
            time.sleep(0.5)
            for j in xrange(0, len(alist)):
                second = proj.find_element_by_id(alist[j]).text
                if (firslist[j] + 55) >= 500:
                    self.assertEqual('500.00', second)
                else:
                    rr = str(firslist[j] + 55) + '.00'
                    self.assertEqual(rr, second)
                firslist[j] = int(second[:-3])

    # 字递减55 下限20
    def test_num_dec(self):
        alist = ('SPAN_5NUM_12', 'SPAN_5NUM_13', 'SPAN_5NUM_14', 'SPAN_5NUM_15', 'SPAN_5NUM_16')
        dec = proj.find_element_by_id('NODE_5CmpFS_26')
        firslist = []

        # 随机设置初始值
        for ele in alist:
            a = random.randint(400, 600)
            firslist.append(a)
            self.keytoimput(ele, a)
        # 执行14次点击
        for i in xrange(0, 14):
            dec.click()
            time.sleep(0.5)
            for j in xrange(0, len(alist)):
                second = proj.find_element_by_id(alist[j]).text
                if (firslist[j] - 55) <= 20:
                    self.assertEqual('20.00', second)
                else:
                    rr = str(firslist[j] - 55) + '.00'
                    self.assertEqual(rr, second)
                firslist[j] = int(second[:-3])

    # 跳转
    def test_changescr(self):
        change = proj.find_element_by_id('NODE_5CmpFS_27')
        change.click()
        time.sleep(0.5)
        vv = proj.find_element_by_id('divfrm2').get_attribute('buse')
        self.assertTrue(vv)
        proj.find_element_by_id('NODE_15FS_0_Comm').click()
        time.sleep(0.5)
        scr1 = proj.find_element_by_id('NODE_0FS_4')
        scr1.click()

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
