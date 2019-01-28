#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: make_hmi_scripts
# Author:    fan
# date:      2019/1/3
# -----------------------------------------------------------
old_words = []
new_words = []
with open("脚本计算器.csv", "r", encoding="gb2312") as csv:
    for line in csv.readlines():
        line_l = line.strip().split(",")
        old_words.append(line_l[1].strip())
        new_words.append(line_l[-1].strip())

print(old_words)
print(new_words)


old_lines = []
new_lines = []
with open("背景定时脚本100ms站号1.txt", "r", encoding="utf-8") as old_file:
    old_lines = old_file.readlines()
    print(old_lines)
    for line in old_lines:
        for i in range(len(old_words)):
            line = line.replace(old_words[i], new_words[i])
            #print(line)
        new_lines.append(line)
    print(new_lines)

with open("背景定时脚本100s站号x.txt", "w", encoding="utf-8") as new_file:
    new_file.writelines(new_lines)

if __name__ == '__main__':
    pass
