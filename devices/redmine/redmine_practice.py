#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: redmine_practice.py
# Author:    fanch
# date:      2018/07/14
# -----------------------------------------------------------

from redminelib import Redmine
import logging as log

log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


def login_redmine(url, user, passwd):
    redmine = Redmine(url, username=user, password=passwd)
    return redmine


def read_project(redmine:Redmine):
    # project.get, 获得特定条件的单个项目
    pro_identifier = 'demp'
    project = redmine.project.get(pro_identifier)
    print('项目标识为demp的项目是：', project)
    # for resouce in sorted(list(project)):
    #     print(resouce[0], ':', resouce[1])

    # project.all, 获取所有公开项目集合
    projects = redmine.project.all()
    print('获得全部项目：'.format(projects))
    print('详细列表: 项目id 项目标识 项目名称')
    # for pro in projects:
    #     print('', pro.id, pro.identifier, pro.name)

    # project.all.export, 导出项目清单
    projects.export('atom', savepath='', filename='redmine projects.atom')


def read_issue(redmine:Redmine):
    pro_identifier = 'demp'
    i_id = 1112
    # issue.get
    issue = redmine.issue.get(i_id)
    issue_dict = dict(issue)
    print('问题/任务编号为{}的项目是: {}'.format(i_id ,issue.subject))
    print('详细信息：\n{}\ndetail:'.format(issue_dict))
    # for key in sorted(issue_dict):
    #     print('{}: {}'.format(key, issue[key]))

    # issue.all 返回所有已打开的问题
    issues = redmine.issue.all(limit=20)
    print('所有问题/任务集合：{}'.format(issues))
    print('列出Redmine上所有已打开问题/任务编号、所属项目、主题：')
    # for iss in issues:
    #     print(iss.id, iss.project['name'], iss.subject, iss.created_on)

    # issue.filter 返回匹配筛选器的一组任务(问题)。
    issues = redmine.issue.filter(project_id=pro_identifier)
    print('项目{} 的问题/任务数量为{}, 清单如下：\n编号 主题'.format(pro_identifier, len(issues)))
    # for iss in issues:
    #     print(iss.id, iss.subject)


def read_membership(redmine:Redmine):
    pro_identifier = 'demp'
    res_id = 100
    membership = redmine.project_membership.get(res_id)
    # print('编号为{}的项目成员为: {}'.format(res_id, membership))
    # memberships = redmine.project_membership.filter(project_id=pro_identifier)
    print('项目为{}的项目成员组为: {}'.format(pro_identifier, memberships))


if __name__ == "__main__":
    urll = "http://192.168.11.118:7777/redmine/"
    usern = "fanchunhui"
    passw = "a6361255"
    identifierr = 'demp'

    red = login_redmine(urll, usern, passw)
    read_project(red)
    read_issue(red)
    read_membership(red)

    # 公司电脑服务器
    # urll = "http://192.168.39.40/redmine"
    # usern = "yonghuyi"
    # passw = "11111111"
    # identifierr = "xiangmuyi"
    # 个人电脑服务器
    # urll = "http://192.168.0.110/redmine"
    # usern = "yonghuyi"
    # passw = "11111111"
    # identifierr = "xiangmuyi"



