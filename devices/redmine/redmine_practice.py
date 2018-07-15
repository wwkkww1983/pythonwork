#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: redmine_practice.py
# Author:    fanch
# date:      2018/07/14
# -----------------------------------------------------------

from redminelib import Redmine

url = 'http://192.168.0.110/redmine'
user = 'yonghuer'
passwd = '111111111'
redmine = Redmine(url, username=user, password=passwd)
project = redmine.project.get('xiangmuyi')    # 必须是'项目标识'
for resouce in list(project):
    print(resouce[0], ':', resouce[1])
issues = project.issues
issue = issues[0]
print('\n\n问题/任务数量: {}\n\n'.format(len(issues)))
for resouce in list(issue):
    print(resouce[0], ':', resouce[1])