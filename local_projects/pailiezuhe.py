#!/usr/bin/python
# -*- coding:utf-8 -*-
# -----------------------------------------------------------
# File Name: pailiezuhe
# Author:    fan
# date:      2018/8/10
# 在一组随机数的组合中选择一个组合使得其各元素之和最接近目标值
# -----------------------------------------------------------
from itertools import combinations, permutations
import random


def get_randnums(lower, upper, numscount):
    nums = []
    for i in range(numscount):
        nums.append(random.randint(lower, upper))
    return nums


def get_combs(nums: list, n: int):
    per = []
    if 3 >= n > 0:
        for i in range(1, n+1):
            per += list(permutations(nums, i))
        print("""
        \n随机数列：{}
        \n组合内元素个数：小于等于{}
        \n生成的组合个数：{}
        \n组合列表：略
        """.format(nums, n, len(per)))
    return per


def pick_fittest_numcom(numcoms:list, targetvalue:int):
    sub_values = [0] * len(numcoms)
    for i in range(len(numcoms)):
        sub_values[i] = abs(sum(numcoms[i]) - targetvalue)
    targetind = sub_values.index(min(sub_values))
    return numcoms[targetind]


if __name__ == '__main__':
    nums = get_randnums(0, 100, 10)
    combs = get_combs(nums, 3)
    targetvalue = 50
    target = pick_fittest_numcom(combs, targetvalue)
    print("最佳(和接近{})的组合： {}".format(targetvalue, target))