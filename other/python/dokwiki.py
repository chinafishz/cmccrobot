# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 08:22:27 2016

@author: chinafishz
"""
from bs4 import BeautifulSoup

s=BeautifulSoup(open("test.html"),'lxml')

temp=s.body
# print temp.span.string
# 


for i in temp.find_all('span'):
    i.unwrap()
    
# for i in temp.find_all('span',lang='EN-US'):
#     i.extract()

for i in temp.find_all('p'):
#     i.unwrap()
    del i['style']
    del i['lang']
    del i['align']
    del i['class']
    i.unwrap()
    
for i in temp.find_all('a'):
    i.unwrap()
    
# for i in temp.find_all('h1'):
#     i.unwrap()

# for i in temp.find_all('h2'):
#     i.unwrap()
for i in temp.find_all('u'):
#     print i,'123'
#     i.unwrap()
    newtag=i
    newtag.string='__'+i.text+'__'
    i.replace_with(newtag)
    i.unwrap()
#     print '__'+i.text+'__'

for i in temp.find_all('b'):
    newtag=i
    newtag.string='**'+i.text+'**'
    i.replace_with(newtag)
    i.unwrap()

for i in temp.find_all('tr'):
#     i.unwrap()
    del i['lang']
    del i['style']
    
for i in temp.find_all('td'):
#     i.unwrap()
    del i['lang']
    del i['style']
    del i['width']
    del i['height']
    
for i in temp.find_all('table'):
#     i.unwrap()
    del i['lang']
    del i['style']
    del i['width']
    del i['class']
    del i['border']






# 第n个cell


cn_table_cell_list={}


# 读取每tr
for cn_tr in temp.table:
    if(cn_tr!='\n'):
        #通过首行获取表格的总行数
        cn_cell_n=0
        cn_str_td=''
        for cn_tb in cn_tr:
             str_cn_tb=str(cn_tb)
             if(cn_tb!='\n' and str_cn_tb!='<td></td>'):          
#                 获取rowspan,colspan
                cn_rowspan=cn_tb.get('rowspan')
                if(cn_rowspan is None):
                    cn_rowspan=1
                cn_colspan=cn_tb.get('colspan')
                if(cn_colspan is None):
                    cn_colspan=1
                    
                if(cn_rowspan>1 or cn_colspan>1):
                    cn_table_cell_list[cn_cell_n]=[int(cn_rowspan),int(cn_colspan)]
                    cn_colspan_temp=int(cn_colspan)
                    for cn_text in cn_tb:
                        if(cn_text!='\n'):
                            cn_str_td=cn_str_td+cn_text
                    while(int(cn_colspan_temp)>1):
#                           解决列合并
                        cn_str_td=cn_str_td+'|1'
                        cn_colspan_temp=cn_colspan_temp-1
                    cn_rowspan=int(cn_rowspan)-1
                    cn_table_cell_list[cn_cell_n][0]=cn_rowspan #要比cn_cell_n+1前,否则cn_cell_n的序号就错了
                    cn_cell_n=cn_cell_n+1
                elif(cn_rowspan==1 and cn_colspan==1):
                    #没有rowspan,colspan属性
                    #rowspan
                    
                    cn_rowspan_temp=cn_table_cell_list[cn_cell_n][0]
                    #colspan
                    cn_colspan_temp=cn_table_cell_list[cn_cell_n][1]
                    if(int(cn_rowspan_temp)>1):
                        if(cn_text!='\n'):
                            cn_str_td=cn_str_td+':::'
                            while(int(cn_colspan_temp)>1):
    #                           解决列合并
                                cn_str_td=cn_str_td+'|2'
                                cn_colspan_temp=cn_colspan_temp-1
                            cn_rowspan_temp=int(cn_rowspan_temp)-1
                            cn_table_cell_list[cn_cell_n][0]=cn_rowspan_temp
                            cn_cell_n=cn_cell_n+1
                    elif(int(cn_rowspan_temp)==1):
                        for cn_text in cn_tb:
                            str_cn_text=cn_text.string
                            print str_cn_text
                            if(cn_text!='\n' and str_cn_text!='<td></td>'):
                                cn_str_td=cn_str_td+cn_text
                                while(int(cn_colspan_temp)>1):
        #                           解决列合并
                                    cn_str_td=cn_str_td+'|3'
                                    cn_colspan_temp=cn_colspan_temp-1
                                cn_cell_n=cn_cell_n+1  
                cn_str_td=cn_str_td+'|'
                
        
        cn_str_td='|'+cn_str_td
        print cn_str_td
        print '======================'
#         print cn_tr
        
                