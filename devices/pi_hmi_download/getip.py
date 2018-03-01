
from os import popen
from time import sleep

def pingip(ipstr):
    result = False
    try:
        output = popen('ping -l 1 -n 1 ' + ipstr).readlines()
        for line in output:
            if str(line).upper().find('TTL') >= 0:
                result = True
                print("'{}',".format(ipstr))
            if str(line).find(u'找不到') >= 0:
                result = False
                print('无法连接ip {}'.format(ipstr))
    except Exception as e:
        print(e)
    return result


if __name__ == "__main__":
    ipl = []
    ippre = '192.168.1.'
    for i in range(1, 256):
        ip = ippre + str(i)
        if pingip(ip):
            ipl.append(ip)

    print(ipl)
