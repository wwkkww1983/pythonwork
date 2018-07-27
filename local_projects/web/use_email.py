#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: use_email
# Author:    fan
# date:      2018/7/6
# -----------------------------------------------------------
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formataddr
from create_html import create_table_html


def send_email(message):
    # 构造MIMEText对象,第一个参数就是邮件正文,第二个参数是MIME的subtype
    # 传入'plain'，最终的MIME就是'text/plain'，最后一定要用utf-8编码保证多语言兼容性。
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['From'] = formataddr(['fanchunhui', 'fanch@we-con.com.cn'])
    msg['To'] = formataddr(['fanch', 'fch.luck@qq.com'])
    msg['Subject'] = '本邮件由python邮件模块生成'
    try:
        server = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
        server.login('fanch@we-con.com.cn', 'king06221988')
        server.sendmail('fanch@we-con.com.cn', ['fch.luck@qq.com'], msg.as_string())
        print('邮件发送成功？')
        server.quit()
    except smtplib.SMTPException as e:
        print('邮件发送失败！出错信息如下：\n', e)


def send_email_with_annex(message, annex_path):
    """
    发送带附件邮件
    :param message: 邮件文本
    :param annex_path: 附件路径
    :return:
    """
    # 构造MIMEText对象,第一个参数就是邮件正文,第二个参数是MIME的subtype
    # 传入'plain'，最终的MIME就是'text/plain'，最后一定要用utf-8编码保证多语言兼容性。
    msg = MIMEMultipart()
    msg['From'] = formataddr(['fanchunhui', 'fanch@we-con.com.cn'])
    msg['To'] = formataddr(['fanch', 'fch.luck@qq.com'])
    msg['Subject'] = '本邮件由python邮件模块生成'
    # 构造邮件正文
    msg.attach((MIMEText(message, 'plain', 'utf-8')))
    # 构造邮件附件
    att1 = MIMEText(open(annex_path, 'rb').read(), 'base64', 'utf-8')
    att1['Content-Type'] = 'application/octet-stream'
    att1['Content-Disposition'] = 'attachment; filename="abc.zip"'
    msg.attach(att1)
    try:
        server = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
        server.login('fanch@we-con.com.cn', 'king06221988')
        server.sendmail('fanch@we-con.com.cn', ['fch.luck@qq.com'], msg.as_string())
        print('邮件发送成功？')
        server.quit()
    except smtplib.SMTPException as e:
        print('邮件发送失败！出错信息如下：\n', e)


def send_email_with_html(message, html):
        # 构造MIMEText对象,第一个参数就是邮件正文,第二个参数是MIME的subtype
        # 传入'plain'，最终的MIME就是'text/plain'，最后一定要用utf-8编码保证多语言兼容性。

        msg = MIMEText(html, 'html', 'utf-8')
        msg['From'] = formataddr(['fanchunhui', 'fanch@we-con.com.cn'])
        msg['To'] = formataddr(['fanch', 'fch.luck@qq.com'])
        msg['Subject'] = '本邮件由python邮件模块生成'
        try:
            server = smtplib.SMTP_SSL('smtp.exmail.qq.com', 465)
            server.login('fanch@we-con.com.cn', 'king06221988')
            server.sendmail('fanch@we-con.com.cn', ['fch.luck@qq.com'], msg.as_string())
            print('邮件发送成功？')
            server.quit()
        except smtplib.SMTPException as e:
            print('邮件发送失败！出错信息如下：\n', e)

if __name__ == '__main__':
    html = create_table_html()
    txt = '你好'
    file = r'C:\Users\fan\Desktop\20180510_AB_1756.zip'
    # send_email(txt)
    # send_email_with_annex('你好', file)
    send_email_with_html(txt, html)
