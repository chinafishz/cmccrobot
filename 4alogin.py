#-*-encoding:utf-8-*-

import time
import requests
from bs4 import BeautifulSoup
import random
import json
import _thread
from requests.auth import HTTPProxyAuth

def cn_json_load(json2, cn_system):
    #     print(json2)
    cn_i = 0
    for i in json2.get('data'):
        ss = i.get('name')
        if ss == cn_system:
            break
        cn_i = cn_i + 1
    #     print(json2.get('data')[cn_i].get('appResAccountList'))
    appResAccountList = json2.get('data')[cn_i].get('appResAccountList').split('|')[0][:-1]
    id_num = json2.get('data')[cn_i].get('id')
    return [appResAccountList, id_num]


def cn_4Asms(r, url, parma, header):
    r.post(url, data=parma, headers=header)
    _thread.exit_thread()


def cn_4ALogin(r, cn_pwd_saw, sendsms1, sendsms2):
    cn_name = "shizhongxia"
    header = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0;  TheWorld 7)',
              'Accept': '*/*', 'Accept-Language': 'zh-CN', 'Accept-Encoding': 'gzip, deflate'}
    proxies = {'http':'http://chinafishz:qwer1234@79d61a65dc3eb552.natapp.cc:29980','https': 'https://chinafishz:qwer1234@79d61a65dc3eb552.natapp.cc:29980'}
    auth=HTTPProxyAuth('chinafishz','qwer1234')
    # sendsms2会变的
    userInfo = sendsms2

    url = 'https://4a.gmcc.net'
    result1 = r.get(url, headers=header, verify=False,proxies=proxies,auth=auth)

    # 获取random_form
    soup1 = BeautifulSoup(result1.text, 'lxml')
    loginForm1 = str(soup1.select('#loginForm')[0].select('input')[0]).split('=')[3].replace('"', '').replace('/>', '')
    #     print(loginForm1)
    # 登陆界面
    url = 'https://4acasp.gmcc.net/jk.do?method=checkUserType&userId=' + cn_name
    a = r.post(url, data={'method': 'checkUserType', 'userId': cn_name}, headers=header, verify=False, proxies=proxies,auth=auth)

    # -----应该返回：SUCCESSG|TshizhongxiaG|T------
    #     print(a.text)
    url = 'https://4acasp.gmcc.net/loginForward.do?target=https://4arz.gmcc.net/first.do?method=login&appCode=IAM000&sendsms=' + sendsms1
    parma = {'random_form': loginForm1, 'loginPage': '/auth/nextlogin.jsp', 'smsNameText': cn_name, 'smsName': cn_name}
    result2 = r.post(url, data=parma, headers=header, verify=False, proxies=proxies,auth=auth)
    soup2 = BeautifulSoup(result2.text, 'lxml')
    loginForm2 = str(soup2.select('#loginForm')[0].select('input')[1]).split('=')[3].replace('"', '').replace('/>', '')
    #     print(loginForm2)
    parma = {'sendsms': sendsms2}
    s = r.post('https://4acasp.gmcc.net/jk.do?method=checkSMSUser&appCode=IAM000', data=parma, headers=header,
               verify=False, proxies=proxies,auth=auth)

    url = 'https://4acasp.gmcc.net/jk.do?method=checkSMSJK&target=https://4arz.gmcc.net/first.do?method=login&authType=noteAuth&appCode=IAM000&loginPage=/auth/nextlogin.jsp&userInfo=' + userInfo
    r.post(url, headers=header, verify=False, proxies=proxies,auth=auth)
    url = 'https://4acasp.gmcc.net/sendSms.do?smsfrom=send&target=https://4arz.gmcc.net/first.do?method=login&authType=noteAuth&appCode=IAM000&loginPage=/auth/nextlogin.jsp'

    # 下面这一步获取短信验证码
    _thread.start_new_thread(cn_4Asms, (r, url, parma, header))

    print('已经发送短信验证码')
    smsinput = input('验证码:')
    #     这里应该要做检查
    print('正在登陆，请稍后...')
    # 验证
    url = 'https://4acasp.gmcc.net/loginServlet.do?target=https://4arz.gmcc.net/first.do?method=login&authType=noteAuth&appCode=IAM000'
    parma = {'compInfo': '', 'random_form': loginForm2, 'loginPage': '/auth/nextUserLogin.jsp', 'userName': cn_name,
             'passWord': '', 'tokenName': cn_name, 'isUsePin': 'true', 'updatePin': 'false', 'tokenpassword': '',
             'pinCode': '', 'smsName': cn_name, 'smsPwd': cn_pwd_saw, 'dynamic_smsPwd': smsinput, 'checkCodeTemp': '',
             'figerName': '', 'challengeName': 'cn_name', 'challegePassword': '', 'vpn': ''}
    result = r.post(url, data=parma, headers=header, verify=False, proxies=proxies,auth=auth)

    params2 = {'method': 'pageQuery',
               '_gt_json': '{"recordType":"object","pageInfo":{"totalRowNum":-1,"pageSize":50,"pageNum":1,"totalPageNum":0,"startRowNum":0,"endRowNum":0},"columnInfo":[{"id":"id","header":"资源ID","fieldName":"id","fieldIndex":"id","sortOrder":null,"hidden":true,"exportable":true,"printable":true},{"id":"hasDueAcc","header":"hasDueAcc","fieldName":"hasDueAcc","fieldIndex":"hasDueAcc","sortOrder":null,"hidden":true,"exportable":true,"printable":true},{"id":"groupName","header":"资源组","fieldName":"groupName","fieldIndex":"groupName","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"name","header":"资源名称","fieldName":"name","fieldIndex":"name","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"ip","header":"IP地址","fieldName":"ip","fieldIndex":"ip","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"restype","header":"资源类型","fieldName":"restype","fieldIndex":"restype","sortOrder":null,"hidden":true,"exportable":true,"printable":true},{"id":"appResAccountList","header":"从帐号列表","fieldName":"id","fieldIndex":"id","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"ssoMode","header":"ssoMode","fieldName":"ssoMode","fieldIndex":"ssoMode","sortOrder":null,"hidden":"true","exportable":true,"printable":true},{"id":"sysResClientList","header":"登录","fieldName":"id","fieldIndex":"id","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"opt","header":"操作","fieldName":"id","fieldIndex":"id","sortOrder":null,"hidden":false,"exportable":true,"printable":true}],"sortInfo":[],"filterInfo":[],"parameters":{},"action":"load"}',
               'queryName': '', 'queryIP': '', 'isQuerySubTree': '1'}
    result2 = r.post('https://4a.gmcc.net/page/resource/appres/appresourceQuery.do', data=params2, headers=header,
                     verify=False, proxies=proxies,auth=auth)
    #     print(result2.text)
    json2 = json.loads(result2.text)
    #     print(json2
    return json2


def cn_iotLogin(r,json2):
    proxies = {'http://chinafishz:qwer1234@79d61a65dc3eb552.natapp.cc:29980',
               'https://chinafishz:qwer1234@79d61a65dc3eb552.natapp.cc:29980'}
    auth = HTTPProxyAuth('chinafishz', 'qwer1234')
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate'}

    appResAccountList=cn_temp[0]
    id_num=cn_temp[1]
    r.post('https://4a.gmcc.net/page/resource/resourceQuery.do?',data={'method':'isAuthDateValid','subaccName':'AGZGT0000829'},headers=header,verify=False,proxies = proxies)
    
    params2={'method':'checkPolicy4JK','resId':id_num,'resAccId':appResAccountList,'date':str(time.time()).replace('.','')+str(random.randint(1,9))}
    result2=r.post('https://4a.gmcc.net/page/jk/sso/appJKLogin.do',data=params2,headers=header,verify=False,proxies = proxies)
   
    params2={'method':'wantGetMACAddress','resId':id_num}
    r.post('https://4a.gmcc.net/sso.do',data=params2,headers=header,verify=False,proxies = proxies)
    
    url2='https://4a.gmcc.net/sso.do?method=appssoData&accID='+appResAccountList+'&resID='+id_num+'&softname=webAppByIE&date='+str(time.time()).replace('.','')+str(random.randint(1,9))
    print('-----------测试是否登陆iot成功-----------')
    s=r.get(url2,headers=header,allow_redirects=True,verify=False,proxies = proxies)
    print(s)
    
#
#
# def cn_ESOPLogin(r,json2,debug=0):
#     proxies = {'http://79d61a65dc3eb552.natapp.cc:29980', 'https://79d61a65dc3eb552.natapp.cc:29980'}
#     header={'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate'}
#     #点击ESOP登陆
#     cn_temp=cn_json_load(json2,u'广东移动NGESOP系统')
#     appResAccountList=cn_temp[0]
#     id_num=cn_temp[1]
# #     print id_num
# #     print appResAccountList
#
#     #同步数据
#     r.post('https://4arz.gmcc.net/keystore.do',data={'method':'getKeyStoreList'},headers=header,verify=False,proxies = proxies)
#     r.post('https://4arz.gmcc.net/page/resource/resourceQuery.do?',data={'method':'isAuthDateValid','subaccName':'AGZGT0000829'},headers=header,verify=False,proxies = proxies)
#
#     params2={'method':'checkPolicy4JK','resId':id_num,'resAccId':appResAccountList,'date':str(time.time()).replace('.','')+str(random.randint(1,9))}
#     result2=r.post('https://4arz.gmcc.net/page/jk/sso/appJKLogin.do',data=params2,headers=header,verify=False,proxies = proxies)
#
# #     params2={'method':'queryLoginJKStatus','resId':id_num,'resAccId':appResAccountList,'date':str(time.time()).replace('.','')+str(random.randint(1,9))}
# #     r.post('https://4a.gmcc.net/page/jk/sso/appJKLogin.do',data=params2,headers=header,verify=False)
#     params2={'method':'wantGetMACAddress','resId':id_num}
#     r.post('https://4arz.gmcc.net/sso.do',data=params2,headers=header,verify=False,proxies = proxies)
#
#     url2='https://4arz.gmcc.net/sso.do?method=appssoData&accID='+appResAccountList+'&resID='+id_num+'&softname=webAppByIE&date='+str(time.time()).replace('.','')+str(random.randint(1,9))
#     params2={'txtMACAddr':'08:00:27:10:3A:FB','txtIPAddr':'10.0.2.15','txtDNSName':'gzshizhongxia'}
#     print('-----------测试是否登陆ESOP成功-----------')
#     s=r.post(url2,data=params2,headers=header,allow_redirects=True,verify=False,proxies = proxies)
#     if(debug==0):
#         print(s)
#     elif(debug==1):
#         print(s.text)




cn_pwd_saw='qWer1@34'
sendsms1='41608446240A6782F2A0F031426EDC066CF24674F3F0586A4D5FF056D75FF4AB'
sendsms2='41608446240A6782F2A0F031426EDC066CF24674F3F0586AF1E3983438A09296B93FF648FA4937967A053D1D504E42BA6069ED5C9B03B580'

r=requests.session()
header={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:44.0) Gecko/20100101 Firefox/44.0','Accept-Language':'en-US,en;q=0.5'}

json2=cn_4ALogin(r,cn_pwd_saw,sendsms1,sendsms2)
# cn_BossLogin(r,json2)
cn_iotLogin(r,json2)


# 查欠费(升级版)
cn_phone='1064887737000'
def iot_chazhuangtai_up(cn_phone):
    proxies = {'http://79d61a65dc3eb552.natapp.cc:29980', 'https://79d61a65dc3eb552.natapp.cc:29980'}
    cn_random='0.'+str(random.randint(100000000000000,999999999999999))+str(random.randint(1,9))
    url='http://10.253.61.8/ngcustcare/chargesrv/common/qryRelateSubs.action?servNumber='+cn_phone+'&isSupportGrp=undefined&random=0.8614928195074256'
    s=r.get(url,headers=header, proxies=proxies,auth=auth)
    soup=BeautifulSoup(s.text,'lxml')

    _status=soup.select('.table_list02')[0].select('input')
    for i in range(len(_status)):
        if _status[i].attrs.get('value')== '广**西思富信息科技有限公司':
            return _status[i+1].attrs.get('value')
#


print(iot_chazhuangtai_up('1064887737004'))



