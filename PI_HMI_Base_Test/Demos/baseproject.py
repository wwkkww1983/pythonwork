# coding:utf8
__author__ = 'admin'

# baseproject 功能检查脚本

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import unittest


ip = '192.168.99.212'
func = 'NODE_0FS_'

class BaseChangeScrTest(unittest.TestCase):
    def setUp(self):
        self.proj = webdriver.Firefox()
        self.proj.maximize_window()
        self.proj.get('http://'+ip+'/')
        time.sleep(1)

    def test_fuc_jump_to_scr(self):
        for i in range(0, 36):
            self.proj.find_element_by_id(func + str(i)).click()
            time.sleep(1)
            screen = 'divfrm%d' % (i+1)
            print(screen)
            im = self.proj.find_element_by_id(screen)
            time.sleep(1)
            s = im.get_attribute('buse')
            self.assertTrue(s)
            sc = im.get_attribute('scrno')

            self.checkfunc(i)

            if i == 35:
                c = i + 2
            else:
                c = i + 1
            self.assertEqual(sc, str(c))
            print(s, sc)
            self.proj.find_element_by_id('NODE_'+str(c)+'FS_0_Comm').click()
            time.sleep(1)
    def checkfunc(self, case):
        if case == 0:      # 表示第一个画面
            pass

    def tearDown(self):
        self.proj.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)


