#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: redmine_practice.py
# Author:    fanch
# date:      2018/07/14
# -----------------------------------------------------------

from redminelib import Redmine


def visit_redmine():
    url = 'http://192.168.0.110/redmine'
    user = 'yonghuer'
    passwd = '111111111'
    redmine = Redmine(url, username=user, password=passwd)
    project = redmine.project.get('xiangmuyi')    # 必须是'项目标识'
    for resouce in sorted(list(project)):
        print(resouce[0], ':', resouce[1])
    issues = project.issues
    issue = issues[1]
    print('\n\n问题/任务数量: {}\n\n'.format(len(issues)))
    for resouce in sorted(list(issue)):
        print(resouce[0], ':', resouce[1])


class Project(object):
    def __init__(self, identifier, url, user, passwd):
        self.identifier = identifier
        redmine = Redmine(url, username=user, password=passwd)
        self.project = redmine.project.get(self.identifier)
        self.print_project_info()

    def print_project_info(self):
        for resouce in sorted(list(self.project)):
            print(resouce[0], ':', resouce[1])
        print('\n\n问题/任务数量: {}\n\n'.format(len(self.project.issues)))

    def count_all(self):
        pass


if __name__ == "__main__":
    visit_redmine()
    # urll = "http://192.168.11.118:7777/redmine/"
    # usern = "fanchunhui"
    # passw = "a6361255"
    # identifierr = 'testgroup'

    # urll = "http://192.168.39.40/redmine"
    # usern = "yonghuyi"
    # passw = "11111111"
    # identifierr = "xiangmuyi"

    # urll = "http://192.168.0.110/redmine"
    # usern = "yonghuyi"
    # passw = "11111111"
    # identifierr = "xiangmuyi"
    # project = Project(identifierr, urll, usern, passw)
