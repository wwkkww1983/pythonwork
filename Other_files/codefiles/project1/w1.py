spath="D:/PythonWork/PYTHONWORKFILES/codefiles/project1/ABC.txt"
a = 0
countline=0
f=open(spath,"r") # 打开并读取
for line in enumerate(f): #对文本逐行枚举
    countline=countline+1  #统计行数
f.close  #关闭文件

f=open(spath,"a")  #打开文本文件
f.write('This is line '+str(countline) +':i like milk.\n')  #写入内容
f.close()  

f=open(spath,"r") # 打开并读取
for line in enumerate(f): #对文本逐行枚举
    print ("第%s行：%s"%line)  #按行号打印每行内容
f.close()
