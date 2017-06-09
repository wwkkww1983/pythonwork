%xls设置，把xls文件的完整路径、sheet名字、纵坐标标签改成所需要的
 path        = 'C:\Users\fan\Desktop\abc.xls'    %xls文件完整路径
 sheet_name  = 'sheet1'                          %工作簿名称
 y_label     = '温度示数'                        %竖轴标签

 %计算和绘图部分，无需修改代码
 plot_title  = sheet_name                        %绘图名称，等于工作簿名称
 [NUM,TXT]   = xlsread(path,sheet_name)          %读取文件形成两个表格
 [hang,lie]  = size(NUM)                         %数值表格的行数、列数
 [legends,le]= size(TXT)                         %文本字段个数
 plot(NUM(1:hang,1),NUM(1:hang,2:lie))
 grid on;
 legend(TXT(1,2:le),0)
 xlabel(TXT(1:1,1:1))
 ylabel(y_label)
 title(plot_title)