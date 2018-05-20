#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: get_JD_product_name_and_price.py
# Author:    fan
# date:      2018/1/24

import requests
from bs4 import BeautifulSoup

# 获取特定商品页面
url = 'http://list.jd.com/list.html?cat=9987,653,655&page=1&delivery=1&trans=1&JL=4_21_0'
request = requests.get(url)

# 解析网页获取物品列表（每条记录包含商品名、价格、评论数、链接等信息）
soup = BeautifulSoup(request.text, "html.parser")
items = soup.select('li.gl-item')
# print(items)
i = 1
for item in items[:2]:

    sku = item.find('div')['data-sku']
    price_url = 'http://p.3.cn/prices/mgets?skuIds=J_' + str(sku)
    price = requests.get(price_url).json()[0]['p']
    name = item.find('div', class_="p-name").find('em').string.strip()
    print(type(item))
    focus = item.find('div', class_='p-focus').find('a').text
    print(focus)
    # price = item.find('div', clsss_='p-price').find('strong', class_='J_price').string
    item_url = 'http:' + item.find('div', class_="p-name").find('a')['href']
    # commit = item.find('div', class_="p-commit").find('a').string
    print("%d. 名称: %s \n   价格: %s 元  \n   链接: %s" % (i, name, price,  item_url))
    if i >= 10:
        break
    else:
        i += 1