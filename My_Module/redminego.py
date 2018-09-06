#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: redminego
# Author:    fan
# date:      2018/7/20
# -----------------------------------------------------------
from redminelib import Redmine
import logging as log
import json

log.basicConfig(level=log.INFO,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s: %(message)s')

STATUS_ID = {"新建": 1, "进行中": 2, "已完成": 3, '审核&评审': 7, '已挂起': 8, '待验证': 9}  # 待定
TRACKER_ID = {"BUG": 1, "任务": 2, "测试": 24}  # 待定


class RedmineGo(object):
    def __init__(self):
        self.redmine = None
        self.project = None
        self.projects = None
        self.issue = None
        self.issues = None
        self.user = None
        self.users = None
        self.membership = None
        self.memberships = None

    def login(self,  url, user, passwd):
        try:
            self.redmine = Redmine(url, username=user, password=passwd)
            log.info('logged in with {} on {}'.format(user, url))
        except Exception as e:
            log.error('fail to log redmine, please check url/username/password. detail: {}'.format(e))

    def get_all_projects(self):
        """
        获取所有项目
        :return:
        """
        try:
            self.projects = self.redmine.project.all()
        except Exception as e:
            log.error('fail to get all projects, please check. detail: {}'.format(e))
        if self.projects:
            i = 0
            dic = {}
            for pro in self.projects:
                dic[pro.identifier] = dict(pro)
                i += i

            with open("projects.json", 'w', encoding='utf-8') as f:
                f.write(json.dumps(dic, ensure_ascii=False, indent=4))
                log.info('projects info loaded')

    def count_projects(self):
        """
        统计公开的项目数量及项目列表
        :return:{项目数量，项目名字清单}
        """
        pro_counts = 0
        pro_names = {}
        try:
            projects = self.projects
            pro_counts = len(projects)
            for pro in projects:
                if pro.name not in pro_names:
                    pro_names[pro.name] = pro.identifier
        except Exception as e:
            log.error('fail to count projects. detail: {}'.format(e))
        return {'pro_counts': pro_counts, 'pro_names': pro_names}

    def get_project_by_identifier(self, proj_identifier):
        """
        根据项目标识返回一个项目(所有信息)
        :param proj_identifier: 项目标识
        :return: 项目
        """
        try:
            self.project = self.redmine.project.get(proj_identifier)
        except Exception as e:
            log.error('fail to get project by project identifier, please check. detail: {}'.format(e))
        return self.project
        # self.print_project_info()

    def get_projects_by_conditions(self, **params):
        """
        按条件过滤返回项目集合,redmine本身不支持filter, 需要调用多个get后提供类似接口
        :param params: 项目过滤条件
        :return: 项目集合
        """
        try:
            self.projects = self.redmine.project.filter(**params)
        except Exception as e:
            log.error('fail to get projects by filter, please check. detail: {}'.format(e))

    def get_project_info(self):
        try:
            for resource in sorted(list(self.project)):
                log.info('{}: {}'.format(resource[0], resource[1]))
            # print('\n\n问题/任务数量: {}\n\n'.format(len(self.project.issues)))
            return True
        except Exception as e:
            log.error('fail to print projects info. plcease check. detail: {}'.format(e))

    def get_all_issues(self):
        """
        统计所有任务数量和任务列表
        :return:
        """
        try:
            self.issues = self.redmine.issue.all()
        except Exception as e:
            log.error('fail to get all issues, please check. detail: {}'.format(e))
        if self.issues:
            i = 0
            dic = {}
            for iss in self.issues:
                dic[iss.id] = dict(iss)
                i += i
            with open("issues.json", 'w', encoding='utf-8') as f:
                f.write(json.dumps(dic, ensure_ascii=False, indent=4))
            log.info('issues info loaded')

    def count_issues(self):
        issue_counts = 0
        issue_names = {}
        try:
            issues = self.issues
            issue_counts = len(issues)
            for iss in issues:
                if iss.subject not in issue_names:
                    issue_names[iss.subject] = iss.id
        except Exception as e:
            log.error('fail to count issues. detail: {}'.format(e))
        return {'issues counts': issue_counts, 'issue names': issue_names}

    def get_issue_by_resource_id(self, resource_id):
        try:
            self.issue = self.redmine.issue.get(resource_id)
        except Exception as e:
            log.error('fail to get issue by resource id, please check. detail: {}'.format(e))

    def get_issues_by_filter(self, **filters):
        try:
            self.issues = self.redmine.issue.filter(**filters)
        except Exception as e:
            log.error('fail to get issues by filter, please check. detail: {}'.format(e))

    @staticmethod
    def get_issue_info(issue):
        try:
            log.info("issue info: {}".format(sorted(list(issue))))
        except Exception as e:
            log.error('fail to print issue info. plcease check. detail: {}'.format(e))

    # def count_issues_created_days_ago(self, project_id, days: int):
    #     """
    #     统计周期内新增问题数
    #     :param project_id: 项目标识
    #     :param days: 统计过去几天内数据
    #     :return: 新增问题列表
    #     """
    #     pass
    #
    # def count_issues_closed_days_ago(self, project_id, days: int):
    #     """
    #     统计周期内关闭问题数
    #     :param project_id: 项目标识
    #     :param days: 统计过去几天内数据
    #     :return:关闭问题列表
    #     """
    #     pass
    #
    # def count_issues_due_days(self, project_id, days):
    #     """
    #     统计周期内仍存续且未解决的问题
    #     :param project_id: 项目标识
    #     :param days: 天数上限
    #     :return:未解决列表
    #     """
    #     pass

    def get_all_users(self):
        """
        生成用户缓存文件
        :return: no return
        """
        # try:
        #     self.users = self.redmine.user.all()
        # except Exception as e:
        #     log.error('fail to get all users, please check. detail: {}'.format(e))
        if self.issues:
            users = {}
            for iss in redminego.issues:
                iss = dict(iss)
                try:
                    if iss['assigned_to']['name'] not in users:
                        users[iss['assigned_to']['name']] = iss['assigned_to']['id']
                except Exception as e:
                    # print(e)
                    # print(iss['id'])    # 存在未指派的任务。。。
                    continue
            # print(users, len(users))
            self.users = users
            with open('users.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(users, ensure_ascii=False, indent=4))
                log.info('users info loaded')

    def count_users(self):
        user_counts = 0
        user_names = {}
        try:
            users = self.users
            user_counts = len(users)
            for usr in users:
                if usr.firstname not in user_names:
                    user_names[usr.lastname + ' ' + usr.firstname] = usr.id
        except Exception as e:
            log.error('fail to count users. detail: {}'.format(e))
        return {'user counts': user_counts, 'user names': user_names}

    @staticmethod
    def get_user_info(usr):
        try:
            log.info("usr info: {}".format(sorted(list(usr))))
        except Exception as e:
            log.error('fail to print user info. plcease check. detail: {}'.format(e))

    def count_memberships(self):
        pass

    def get_membership_by_resource_id(self, resource_id):
        pass

    @staticmethod
    def get_membership_info(membership):
        pass


if __name__ == '__main__':
    urll = "http://192.168.11.118:7777/redmine/"  # 公司Redmine服务器
    usern = "fanchunhui"
    passw = "a6361255"
    project_identifierr = 'demp'
    res_id = 1608
    names = ['范 春回', '黄 海燕', '王 艳如', '陶 艳杰', '兰 秋琳', '李 云', '赖 永珍', '叶 倩', '张 艳虹', '贾 小洁']


    def get_ones_issues(names):
        with open('issues.json', 'r', encoding='utf-8') as f:
            issues = json.loads(f.read())
        print('{}, {}, {}, {}, {}, {}, {}'.format(
            '项目名称', '任务id', '任务主题', '任务类型', '分配给', '状态', '计划完成时间'))
        for issid, iss in issues.items():
            if "assigned_to" in iss.keys():
                if iss["assigned_to"]['name'] in names \
                        and iss['status']['id'] in [1, 2, 7, 9] \
                        and iss["tracker"]["id"] in [1, 2, 24]:
                    if "due_date" not in iss.keys():
                        iss["due_date"] = "无"
                    print('{}, {}, {}, {}, {}, {}, {}'.format(iss['project']['name'],
                                                              issid,
                                                              iss['subject'],
                                                              iss["tracker"]['name'],
                                                              iss["assigned_to"]['name'],
                                                              iss['status']['name'],
                                                              iss["due_date"]))

    # urll = "http://192.168.39.40/redmine"    # 公司pc私人Redmine服务器
    # usern = "admin"
    # passw = "admin111"

    redminego = RedmineGo()
    redminego.login(urll, usern, passw)
    redminego.get_all_projects()
    redminego.get_all_issues()
    redminego.get_all_users()

    # 获取全部项目
    # redminego.get_all_projects()
    # print(redminego.count_projects())

    # redminego.get_project_by_identifier(project_identifierr)
    # print(dict(redminego.project))

    # redminego.get_issue_by_resource_id(res_id)
    # iss = dict(redminego.issue)
    # for key, value in iss.items():
    #     print(key, value)

    # redminego.get_all_issues()
    # # print(redminego.count_issues())

    # 通过过滤器进行任务筛选，灵活组合条件可以完成绝大部分筛选任务
    # redminego.get_issues_by_filter(project_id='demp',
    #                                tracker_id=None,
    #                                status_id="1",
    #                                assigned_to_id="35",    # 被指派人ID，这里不能通过指派人姓名进行过滤
    #                                # start_date='><2018-07-31|2018-08-28',
    #                                # due_date='><2018-07-31|2018-08-28'
    #                                )
    # print(redminego.count_issues())

    # for iss in redminego.issues:
    #     redminego.get_issue_info(iss)

    # redminego.get_all_users()    # 暂无访问公司服务器权限
    # print(redminego.count_users())
    # print(redminego.get_user_info(redminego.users[1]))

    get_ones_issues(names)
