
def func():
    """
    判断一个输入的字符串是否全由0~9构成，如果是，则输入正确
    如果否，则提示其中的非数字字符
    :return: None
    """
    a = input('>>>操作开始(输入"quit"退出程序)<<<\n请输入一个整数：')
    b = 0
    c = []
    if a == 'exit':
        return
    else:
        pass
    a_list = [i for i in a]
    for i in a_list:
        if 48 <= ord(i) <=57:
            b += 1
            c += i
    try:    
        if b == len(a):
            if b != 0:
                print('info: 输入内容为:{}\n>> 数字输入正确'.format(a))
            else:
                print('info: 输入内容为空，输入无效')
        
        else:
            raise Exception('info: 输入内容为"{}",包含含非数字字符{}，请重新输入'.format(a,list(set(a).difference(set(c)))))
    except Exception as e:
        print(e)
    print('>>>操作结束<<<\n')
    func()    

if __name__ == '__main__':
    print(func.__doc__)
    func()
