'''
names = ['M','B','T']
for name in names:
    print(name)
'''   
sum = 0
for x in range(20):  #打印奇数
    if x%2 == 0:
        continue
    print (x)
print('end')

'''
sum1 = 0
n = 99
while n > 0:
    sum1 = sum1 + n
    n = n - 1
print(sum1)

n = 1
while n <= 100:
    if n > 10: # 当n = 11时，条件满足，执行break语句
        break # break语句会结束当前循环
    print(n)
    n = n + 1
print('END')
'''