#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: redmine_methods
# Author:    fan
# date:      2018/9/4
# -----------------------------------------------------------
from redminego import RedmineGo
import json


def get_some_issues(status_id_in: list, tracker_id_in: list, assigned_to_name_in: list, fields: list):
    """
    根据任务状态，任务类型，被指派人列表筛选，按可选字段显示和打印
    :param status_id_in:
    :param tracker_id_in:
    :param assigned_to_name_in:
    :param fields:
    :return:
    """
    with open('issues.json', 'r', encoding='utf-8') as f:
        issues = json.loads(f.read())
    with open('users.json', 'r', encoding='utf-8') as f1:
        users = json.loads(f1.read())
    user_ids = [users[i] for i in assigned_to_name_in]
    fie = ('|||'.join(fields) + '|||tester')
    new1 = []
    new2 = []
    for issid, iss in issues.items():
        if "due_date" not in iss.keys():
            iss["due_date"] = "无"
        if "assigned_to" in iss.keys():
            # 包含被指派人的任务才能正常进行绩效统计
            if iss['status']['id'] in status_id_in and iss["tracker"]["id"] in tracker_id_in:
                # 状态、任务类型

                if iss["assigned_to"]['name'] in assigned_to_name_in:
                    # 跟踪项：被指派人在测试部范围内
                    new = []
                    for i in fields:
                        u = i.split(' ')
                        if len(u) == 1:
                            new.append(str(iss[u[0]]))
                        if len(u) == 2:
                            new.append(str(iss[u[0]][u[1]]))
                    new.append('无')
                    new1.append('|||'.join(new))
                else:
                    # 被指派人不是测试部范围，要查看字段“测试人员”是否为测试部人员：
                    try:
                        for i in iss["custom_fields"]:
                            if i['id'] == 7:
                                if int(i['value']) in user_ids:
                                    new = []
                                    for x in fields:
                                        u = x.split(' ')
                                        if len(u) == 1:
                                            new.append(str(iss[u[0]]))
                                        if len(u) == 2:
                                            new.append(str(iss[u[0]][u[1]]))
                                    for key in users.keys():
                                        if users[key] == int(i['value']):
                                            new.append(key)
                                    new2.append('|||'.join(new))
                    except Exception as e:
                        pass

    x = [fie] + new1 + new2
    for i in x:
        print(i)
    return x


if __name__ == '__main__':
    urll = "http://192.168.11.118:7777/redmine/"  # 公司Redmine服务器
    usern = "fanchunhui"
    passw = "a6361255"
    project_identifierr = 'demp'
    res_id = 1608
    status_ids = [1, 2, 7, 9]
    tracker_ids = [1, 2, 24]
    field_list = ['id', 'project name', 'subject', 'tracker name',
                  'assigned_to name', 'author name', 'status name', 'due_date']
    assigned_names = ['范 春回', '黄 海燕', '王 艳如', '陶 艳杰', '兰 秋琳',
                      '李 云', '赖 永珍', '叶 倩', '张 艳虹', '贾 小洁']

    redminego = RedmineGo()
    redminego.login(urll, usern, passw)
    # redminego.get_all_projects()
    # redminego.get_all_issues()
    # redminego.get_all_users()

    get_some_issues(status_ids, tracker_ids, assigned_names, field_list)
