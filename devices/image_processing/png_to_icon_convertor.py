#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: png_to_icon_convertor
# Author:    fan
# date:      2019/6/20 020
# -----------------------------------------------------------
from PIL import Image
import os
size = (128, 128)
pic_dir = r"Z:\MyworkSpace\pythonwork\devices\image_processing\图标\PNGS"
for pic in os.listdir(pic_dir):
    src_pic = os.path.join(pic_dir, pic)
    if os.path.splitext(pic)[1] == ".png":
        tgt_pic = os.path.splitext(src_pic)[0].replace("PNGS", "ICONS") + ".ico"
        img = Image.open(src_pic)
        img.thumbnail(size)
        img.save(tgt_pic)
if __name__ == '__main__':
    pass
