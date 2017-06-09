# -*- coding: utf-8 -*-

print(u'''
\t1.静夜思

床前明月光，
疑是地上霜。
举头望明月，
低头思故乡。\n''')


s1 = 72
s2 = 85
r = (s2 - s1) / s1 * 100
print('''\t2.小明的成绩
小明去年的成绩是%d分,
今年的成绩是%d分。
今年的成绩比去年提高了%2.1f%%。''' % (s1, s2, r))

a = int(input('Please input a integer:'))
print(a)