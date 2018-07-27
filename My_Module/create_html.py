#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: create_html
# Author:    fan
# date:      2018/7/24
# -----------------------------------------------------------
import webbrowser
import time


def create_table_html():
    title = "主标题"
    txt = "描述"
    table_title = '表格标题'
    table_fields = ['字段1', '字段2']
    table_data = [['行1列1', '行1列2'], ['行2列1', '行2列2'], ['行3列1', '行3列2']]

    table_body_field = []
    table_body_data = []
    for field in table_fields:
        table_body_field.append("<th>{}</th>".format(field))
    table_body_field = ["<tr>"] + table_body_field + ["</tr>"]  # 生成表头文本

    for row in table_data:
        temp = []
        for item in row:
            temp.append("<td>{}</td>".format(item))
        temp = ["<tr>"] + temp + ["</tr>"]
        table_body_data += temp

    table_body = ''.join(table_body_field) + ''.join(table_body_data)  # 生成表格体

    html_start = """
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>"""

    html_title = "<h1>{}</h1>".format(title)
    html_txt = "<p>{}</p>".format(txt)

    html_table = """
    <h2>{}</h2>
    <table border="1">
    <tbody>
    {}
    </tbody>
    </table>""".format(table_title, table_body)

    html_end = """
    </div>
    </body>
    </html>"""

    _html = html_start + html_title + html_txt + html_table + html_end
    return _html
if __name__ == '__main__':
    html = create_table_html()
    with open("table.html", 'w', encoding='utf-8') as f:
        f.write(html)
    print(html)
    time.sleep(2)
    webbrowser.open("file:///E:\MyWorkPlace\pythonwork\local_projects\web\\table.html")
