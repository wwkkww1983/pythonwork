#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: redminego
# Author:    fan
# date:      2018/7/20
# -----------------------------------------------------------
from redminelib import Redmine
import logging as log

log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')


class RedmineGo(object):
    def __init__(self, url, user, passwd):
        self.redmine = None
        self.project = None
        self.projects = None
        self.issue = None
        self.membership = None
        try:
            self.redmine = Redmine(url, username=user, password=passwd)
        except Exception as e:
            log.error('fail to log redmine, please check url/username/password. detail: {}'.format(e))

    def get_project_by_identifier(self, proj_identifier):
        try:
            self.project = self.redmine.project.get(proj_identifier)
        except Exception as e:
            log.error('fail to get project, please check. detail: {}'.format(e))
        return self.project
        # self.print_project_info()

    def get_project_by_conditions(self, **factors):
        """

        :param factors: member: str, member
        :return: redmine.project
        """

    def get_all_projects(self):
        try:
            self.projects = self.redmine.project.all()
        except Exception as e:
            log.error('fail to get projects, please check. detail: {}'.format(e))

    def get_projects_info(self):
        try:
            for resouce in sorted(list(self.project)):
                log.info('{}: {}'.format(resouce[0], resouce[1]))
            # print('\n\n问题/任务数量: {}\n\n'.format(len(self.project.issues)))
            return True
        except Exception as e:
            log.error('fail to print projects info. plcease check. detail: {}'.format(e))

    def count_all_projects(self):
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
            log.info('fail to count projects. detail: {}'.format(e))
        return {'pro_counts': pro_counts, 'pro_names': pro_names}

    def count_issues_created_days_ago(self, project_id, days: int):
        """
        统计周期内新增问题数
        :param project_id: 项目标识
        :param days: 统计过去几天内数据
        :return: 新增问题列表
        """
        pass

    def count_issues_closed_days_ago(self, project_id, days: int):
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
    project_identifierr = 'demp'

    redminego = RedmineGo(urll, usern, passw)
    print(redminego.count_all_projects())
