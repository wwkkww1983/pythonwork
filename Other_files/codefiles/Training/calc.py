def fib(n):
    """输出一个基于n的斐波纳数列"""
    a,b=0,1
    while b<n:
      print(a,b)
      a,b=b,a+b

fib(100)

def myprint(m):
    #输出一个数m的平方的值
    i= m*m
    s='The value of i is'
    print(s,i)

myprint(10)

def print0(l):
    #返回0
    return 0
