# !/usr/bin/env python
# _*_ coding: utf-8 _*_

image_path = r'C:\Users\fan\OneDrive\pythonwork\local_projects\pil_module\BingWallpaper-2017-03-23.jpg'
from PIL import Image


def create_small(im_path, im_size):
    """定义函数,给定图片路径返回一定大小缩略图"""

    im = Image.open(im_path, 'r')
    im_attribute = [im.format, im.size, im.mode]
    print(im_attribute)
    im.thumbnail(im_size, resample = 3)
    #关于图片质量参数的说明（由于与目前学习内容无相关性，不深究）http://www.youdaili.net/python/13185.html
    im.save('3.jpg', 'JPEG')
image_size = (400,400)
create_small(image_path, image_size)