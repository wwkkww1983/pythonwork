#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: pil_ocr
# Author:    fan
# date:      2018/5/29
# -----------------------------------------------------------
from PIL import Image
from pytesseract.pytesseract import image_to_string


def open_image(ipath):
    im = Image.open(ipath)
    # im.show()
    return im


def image2str(image, lan='eng'):
    text = image_to_string(image, lang=lan)
    return text


if __name__ == '__main__':
    img = open_image('number.png')
    print(image2str(img))
