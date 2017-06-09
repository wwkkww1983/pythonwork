def power(x):
    return x * x


#a = power(5)


def power_1(x, n=2):
    s = 1
    while n > 0:
        n -= 1
        s = s * x
    return s

b = power_1(5)
print(b)
