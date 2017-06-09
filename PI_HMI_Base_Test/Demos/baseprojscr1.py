# coding:utf8
__author__ = 'admin'

# 写答案以及对答案

from selenium import webdriver
import time
import unittest
import urllib

keyb1000span = ('NODE_1000KY_3', 'NODE_1000KY_5', 'NODE_1000KY_4', 'NODE_1000KY_1', 'NODE_1000KY_10',
                'NODE_1000KY_9', 'NODE_1000KY_6', 'NODE_1000KY_16', 'NODE_1000KY_15', 'NODE_1000KY_11',
                'NODE_1000KY_8', 'NODE_1000KY_14')                      # 0123456789.-
# enter enter del clr esc
keyb1000cont = ('NODE_1000KY_2', 'NODE_1000KY_23', 'NODE_1000KY_7', 'NODE_1000KY_12', 'NODE_1000KY_13')
keyb1000 = ('SPAN_1000STR_24', 'SPAN_1000STR_25', 'SPAN_1000STR_26')    # 最小值id， 最大值id， 输入值id


ip = '192.168.99.212'
ipp = 'http://'+ip+'/'
proj = webdriver.Firefox()
proj.get('http://'+ip+'/')
proj.maximize_window()
proj.implicitly_wait(20)
scr1 = proj.find_element_by_id('NODE_0FS_0')
scr1.click()
time.sleep(1)

class ButtonTest(unittest.TestCase):
    def setUp(self):
        pass

    # off按钮
    def test_off_button(self):
        onbutton = proj.find_element_by_id('NODE_1BS_0')
        onbutton.click()
        time.sleep(1)
        onbutton.click()
        des = onbutton.get_attribute('src')
        self.assertEqual(des, ipp + 'img/00004.png')

    # on按钮
    def test_on_button(self):
        offbutton = proj.find_element_by_id('NODE_1BS_6')
        offbutton.click()
        time.sleep(1)
        offbutton.click()
        des = offbutton.get_attribute('src')
        self.assertEqual(des, ipp + 'img/00005.png')

    def test_reset100ms(self):
        reset = proj.find_element_by_id('NODE_1BS_9')
        scr = reset.get_attribute('src')
        reset.click()
        tmp = proj.find_element_by_id('NODE_1BS_9')
        des = tmp.get_attribute('src')
        # self.assertNotEqual(scr, des)       # 100ms无法检查
        time.sleep(0.2)
        reset = proj.find_element_by_id('NODE_1BS_9')
        des = reset.get_attribute('src')
        self.assertEqual(scr, des)

    # 500ms复位
    def test_reset500ms(self):
        reset = proj.find_element_by_id('NODE_1BS_11')
        scr = reset.get_attribute('src')
        reset.click()
        time.sleep(0.1)
        tmp = proj.find_element_by_id('NODE_1BS_11')
        des = tmp.get_attribute('src')
        self.assertNotEqual(scr, des)
        time.sleep(0.5)
        reset = proj.find_element_by_id('NODE_1BS_11')
        des = reset.get_attribute('src')
        self.assertEqual(scr, des)

    # 1000ms复位
    def test_reset1000ms(self):
        reset = proj.find_element_by_id('NODE_1BS_13')
        scr = reset.get_attribute('src')
        reset.click()
        time.sleep(0.5)
        tmp = proj.find_element_by_id('NODE_1BS_13')
        des = tmp.get_attribute('src')
        self.assertNotEqual(scr, des)
        time.sleep(1.5)
        reset = proj.find_element_by_id('NODE_1BS_13')
        des = reset.get_attribute('src')
        self.assertEqual(scr, des)

    # 切换按钮
    def test_switch(self):
        for i in xrange(0, 3):
            reset = proj.find_element_by_id('NODE_1BS_15')
            scr = reset.get_attribute('src')
            reset.click()
            time.sleep(1)
            tmp = proj.find_element_by_id('NODE_1BS_15')
            des = tmp.get_attribute('src')
            self.assertNotEqual(scr, des)
            time.sleep(0.5)

    # 反向显示
    def test_reverse(self):
        for i in xrange(0, 3):
            reset = proj.find_element_by_id('NODE_1BS_16')
            reset.click()
            scr = reset.get_attribute('src')
            onbutton = proj.find_element_by_id('NODE_1BS_0')
            des = onbutton.get_attribute('src')
            self.assertNotEqual(scr, des)
            time.sleep(0.5)

    # 锁控制和显示
    def test_swich_show_lock_png(self):
        contr = proj.find_element_by_id('NODE_1BS_67')    # 按下控制按钮
        s = contr.get_attribute('src')
        if '00004.png' in s:
            loc = proj.find_element_by_id('NODE_1BS_66')
            c = loc.get_attribute('src')
            self.assertEqual(c, ipp + 'img/lock.png')

            contr.click()
            time.sleep(0.5)

            loc = proj.find_element_by_id('NODE_1BS_66')
            c = loc.get_attribute('src')
            self.assertEqual(c, ipp + 'img/00004.png')
        else:
            loc = proj.find_element_by_id('NODE_1BS_66')
            c = loc.get_attribute('src')
            self.assertEqual(c, ipp + 'img/00004.png')

            contr.click()
            time.sleep(0.5)

            loc = proj.find_element_by_id('NODE_1BS_66')
            c = loc.get_attribute('src')
            self.assertEqual(c, ipp + 'img/lock.png')

    # 间接写寻址
    def test_Indirect_addressing_read(self):
        readlist = ('NODE_1BS_29', 'NODE_1BS_30', 'NODE_1BS_31', 'NODE_1BS_32',
                    'NODE_1BS_33', 'NODE_1BS_34', 'NODE_1BS_35')
        for i in xrange(3, 10):
            contr = proj.find_element_by_id('NODE_1BS_20')
            s = contr.get_attribute('src')
            input = proj.find_element_by_id('NODE_1NUM_25')
            input.click()
            time.sleep(0.5)
            proj.find_element_by_id(keyb1000span[i]).click()
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000cont[0]).click()          # enter按键
            time.sleep(0.2)
            loc = proj.find_element_by_id(readlist[i - 3]).click()
            time.sleep(0.5)
            c = proj.find_element_by_id(readlist[i - 3]).get_attribute('src')
            time.sleep(0.2)
            contr = proj.find_element_by_id('NODE_1BS_20')
            s = contr.get_attribute('src')
            self.assertEqual(s, c)

    # 间接读寻址
    def test_Indirect_addressing_write(self):
        writelist = ('NODE_1BS_27', 'NODE_1BS_47',  'NODE_1BS_48',  'NODE_1BS_49',
                     'NODE_1BS_50', 'NODE_1BS_51', 'NODE_1BS_52', 'NODE_1BS_53', 'NODE_1BS_54')
        for i in xrange(1, 10):
            contr = proj.find_element_by_id(writelist[i - 1])   # 第一次获取
            s = contr.get_attribute('src')
            input = proj.find_element_by_id('NODE_1NUM_24')     # 点击弹出
            input.click()
            time.sleep(0.5)
            proj.find_element_by_id(keyb1000span[i]).click()    # 输出1~9
            time.sleep(0.2)
            proj.find_element_by_id(keyb1000cont[0]).click()    # enter按键
            time.sleep(0.2)

            proj.find_element_by_id('NODE_1BS_22').click()      # 点击
            time.sleep(0.5)

            contr = proj.find_element_by_id(writelist[i - 1])
            d = contr.get_attribute('src')

            if '00004.png' in s:
                self.assertEqual(d, ipp + 'img/00005.png')
            else:
                self.assertEqual(d, ipp + 'img/00004.png')

            self.assertNotEqual(d, s)

    def tearDown(self):
        time.sleep(1)

if __name__ == '__main__':
    unittest.main()
    proj.quit()