%xls���ã���xls�ļ�������·����sheet���֡��������ǩ�ĳ�����Ҫ��
 path        = 'C:\Users\fan\Desktop\abc.xls'    %xls�ļ�����·��
 sheet_name  = 'sheet1'                          %����������
 y_label     = '�¶�ʾ��'                        %�����ǩ

 %����ͻ�ͼ���֣������޸Ĵ���
 plot_title  = sheet_name                        %��ͼ���ƣ����ڹ���������
 [NUM,TXT]   = xlsread(path,sheet_name)          %��ȡ�ļ��γ��������
 [hang,lie]  = size(NUM)                         %��ֵ��������������
 [legends,le]= size(TXT)                         %�ı��ֶθ���
 plot(NUM(1:hang,1),NUM(1:hang,2:lie))
 grid on;
 legend(TXT(1,2:le),0)
 xlabel(TXT(1:1,1:1))
 ylabel(y_label)
 title(plot_title)