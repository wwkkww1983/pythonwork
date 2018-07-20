#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: redminego
# Author:    fan
# date:      2018/7/20
# -----------------------------------------------------------
from redminelib import Redmine
class RedmineGo(object):
    def __init__(self, url, user, passwd):
        self.redmine = None
        self.project = None
        try:
            self.redmine = Redmine(url, username=user, password=passwd)
        except Exception as e:
            print('fail to log redmine, please check url/username/password. detail: {}'.format(e))

    def get_project_by_identifier(self, identifier):
        try:
            self.project = self.redmine.project.get(identifier)
        except Exception as e:
            print('fail to get project, please check. detail: {}'.format(e))
        return self.project
        # self.print_project_info()

    def print_projects_info(self):
        try:
            for resouce in sorted(list(self.project)):
                print(resouce[0], ':', resouce[1])
            # print('\n\n问题/任务数量: {}\n\n'.format(len(self.project.issues)))
            return True
        except Exception as e:
            print('fail to print projects info. plcease check.')

    def count_projects(self):
        """
        统计公开的项目数量及项目列表
        :return:{项目数量，项目名字清单}
        """
        pro_counts = 0
        pro_names = []
        try:
            projects = self.redmine.project.all()
            pro_counts = len(projects)
            for pro in projects:
                if pro.name not in pro_names:
                    pro_names.append(pro.name)
        except Exception as e:
            print('fail to count projects. detail: {}'.format(e))
        return {'pro_counts': pro_counts, 'pro_names': pro_names}

    def count_issues_created_days_ago(self, project_id, days):
        """
        统计周期内新增问题数
        :param project_id: 项目标识
        :param days: 统计过去几天内数据
        :return: 新增问题列表
        """
        pass

    def count_issues_closed_days_ago(self, project_id, days):
        """
        统计周期内关闭问题数
        :param project_id: 项目标识
        :param days: 统计过去几天内数据
        :return:关闭问题列表
        """
        pass

    def count_issues_due_days(self, project_id, days):
        """
        统计周期内仍存续且未解决的问题
        :param project_id: 项目标识
        :param days: 天数上限
        :return:未解决列表
        """
        pass


if __name__ == '__main__':
    urll = "http://192.168.11.118:7777/redmine/"
    usern = "fanchunhui"
    passw = "a6361255"
    identifierr = 'demp'

    redminego = RedmineGo(urll, usern, passw)
    print(redminego.count_projects())
