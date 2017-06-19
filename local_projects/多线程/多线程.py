# !/usr/bin/python
# -*- coding: utf-8 -*-
# 在Python中，多线程的意义在于当程序需要进行频繁的IO等待时，可以用多线程同时进行IO操作和其他操作
from time import ctime, sleep
import threading

def music(func):
    for i in range(5):
        print("I was listening to music %s. %s" % (func, ctime()))
        sleep(4)

def movie(func):
    for i in range(4):
        print("I was at the movies %s! %s" % (func, ctime()))
        sleep(5)

threads = []    # 建立线程数组
t1 = threading.Thread(target=music, args=('Poker face',))  # 线程1指定函数、参数
threads.append(t1)  # 装载线程1
t2 = threading.Thread(target=movie, args=('Games of Throne',))  # 线程2指定函数、参数
threads.append(t2)  # 装载线程1


if __name__ == '__main__':
    for t in threads:  # 循环执行线程数组中的线程
        t.setDaemon(True)  # 将线程声明为守护线程
        t.start()  # 开始线程
    t.join()  # 在子线程执行完成之前，父线程将一直被阻塞
    print("all over %s" % ctime())
