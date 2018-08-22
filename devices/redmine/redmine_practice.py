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


def get_project(redmine: Redmine, pro_id=None):
    if pro_id:
        # project.get, 获得特定条件的单个项目
        pro_identifier = pro_id
        project = redmine.project.get(pro_identifier)
        log.info('项目标识为{}的项目是：{}'.format(pro_identifier, project))
        log.info('项目详细信息: 属性 值')
        for resource in sorted(list(project)):
            log.info('{}: {}'.format(resource[0], resource[1]))
        return project
    else:
        # project.all, 获取所有公开项目集合
        projects = redmine.project.all()
        log.info('获得全部公开项目：{}'.format(len(projects)))
        log.info('详细列表: 项目id 项目标识 项目名称')
        for pro in projects:
            log.info('{} {} {}'.format(pro.id, pro.identifier, pro.name))
        return projects


def export_project(projs, fmtt, path, filefullname):
    # project.all.export, 导出项目清单,只适用全部项目导出，不支持单个项目导出
    projs.export(fmt=fmtt, savepath=path, filename=filefullname)
    return 0


def get_issue(redmine: Redmine, pro_id=None, iss_id=None):
    issues = []
    if iss_id:
        # issue.get 返回对应id的任务
        i_id = iss_id
        issue = redmine.issue.get(i_id)
        issue_dict = dict(issue)
        log.info('问题/任务编号为{}的项目是: {}'.format(i_id, issue.subject))
        # log.info('详细信息：\n{}\ndetail:'.format(issue_dict))
        log.info('详细信息：属性 值'.format(issue_dict))
        for key in sorted(issue_dict):
            log.info('{}: {}'.format(key, issue[key]))
        issues.append(issue)

    if pro_id:
        # issue.filter 返回匹配筛选器的一组任务(问题)，例：同一项目的所有问题
        pro_identifier = pro_id
        issue = redmine.issue.filter(project_id=pro_identifier)
        log.info(('项目{} 的问题/任务数量为{}, 清单如下：\n编号 主题'.format(pro_identifier, len(issue))))
        for iss in issue:
            log.info(iss.id, iss.subject)
        issues = list(issue)

    if (not iss_id) and (not pro_id):
        # issue.all 返回所有已打开的问题
        issue = redmine.issue.all()
        log.info('所有问题/任务集合：{}'.format(issue))
        log.info('列出Redmine上所有已打开问题/任务编号、所属项目、主题、创建时间')
        for iss in issue:
            log.info('{} {} {} {}'.format(iss.id, iss.project['name'], iss.subject, iss.created_on))
        issues = list(issue)

    return issues


def get_membership(redmine:Redmine, pro_id):
    # 通过项目标识查询项目成员
    pro_identifier = pro_id
    # res_id = 100
    # membership = redmine.project_membership.get(res_id)
    # log.info('编号为{}的项目成员为: {}'.format(res_id, membership))
    memberships = redmine.project_membership.filter(project_id=pro_identifier)
    log.info('项目为{}的项目成员组为: 编号 姓名'.format(pro_identifier))
    for mem in memberships:
        log.info('{} {}'.format(mem.id, mem.user))
    return memberships


if __name__ == "__main__":
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

    urll = "http://192.168.11.118:7777/redmine/"
    usern = "fanchunhui"
    passw = "a6361255"
    project_identifierr = 'demp'
    red = login_redmine(urll, usern, passw)

    # pros = get_project(red)
    # ex_fmt = 'html'
    # export_project(pros, ex_fmt, '', 'projects.' + ex_fmt)

    # pros = get_project(red, project_identifierr)

    # issues = get_issue(red)

    # issue = get_issue(red, iss_id=1522)

    get_membership(red, project_identifierr)




