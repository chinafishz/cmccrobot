
#-*-encoding:utf-8-*-
import requests
from bs4  import BeautifulSoup
import random
import json
import time
import _thread


cn_pwd_saw='qWer1@34'

sendsms2='41608446240A6782F2A0F031426EDC066CF24674F3F0586AF1E3983438A09296068B27CDC69779838A7C55CD262073C96CF24674F3F0586A33D411E96614BA993A16DFEB2EF9D75B55FBFB72B350DD6D'
          
    
def cn_4Asms(r,url,parma,header):
        r.post(url,data=parma,headers=header) 
        _thread.exit_thread()
        
def cn_4ALogin(r,cn_pwd_saw,sendsms2):
    cn_name="shizhongxia"
    header={'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0;  TheWorld 7)','Accept':'*/*','Accept-Language':'zh-CN','Accept-Encoding':'gzip, deflate'}
    sendsms1='41608446240A6782F2A0F031426EDC066CF24674F3F0586A4D5FF056D75FF4AB'
    #sendsms2会变的
    userInfo=sendsms2
    
    
    
    url='https://4a.gmcc.net'
    result1=r.get(url,headers=header,verify=False)
 
    #获取random_form
    soup1=BeautifulSoup(result1.text,'lxml')
    loginForm1=str(soup1.select('#loginForm')[0].select('input')[0]).split('=')[3].replace('"','').replace('/>','')
#     print soup1.select('#loginForm')[0].select('input')[0]
    print(loginForm1)
    #登陆界面
    url='https://4acasp.gmcc.net/jk.do?method=checkUserType&userId='+cn_name
    a=r.post(url,data={'method':'checkUserType','userId':cn_name},headers=header,verify=False)

    #-----应该返回：SUCCESSG|TshizhongxiaG|T------
#     print(a.text
    url='https://4acasp.gmcc.net/loginForward.do?target=https://4a.gmcc.net/first.do?method=login&appCode=IAM000&sendsms='+sendsms1
    parma={'random_form':loginForm1,'loginPage':'/auth/nextlogin.jsp','smsNameText':cn_name,'smsName':cn_name}
    result2=r.post(url,data=parma,headers=header,verify=False)
    soup2=BeautifulSoup(result2.text,'lxml')
#     print soup2
    loginForm2=str(soup2.select('#loginForm')[0].select('input')[1]).split('=')[3].replace('"','').replace('/>','')
#     print loginForm2
    parma={'sendsms':sendsms2}
    s=r.post('https://4acasp.gmcc.net/jk.do?method=checkSMSUser',data=parma,headers=header,verify=False)
    
    url='https://4acasp.gmcc.net/jk.do?method=checkSMSJK&target=https://4a.gmcc.net/first.do?method=login&authType=noteAuth&appCode=IAM000&loginPage=/auth/nextlogin.jsp&userInfo='+userInfo
    r.post(url,headers=header,verify=False)
    url='https://4acasp.gmcc.net/sendSms.do?smsfrom=send&target=https://4a.gmcc.net/first.do?method=login&authType=noteAuth&appCode=IAM000&loginPage=/auth/nextlogin.jsp'

    #下面这一步获取短信验证码
    _thread.start_new_thread(cn_4Asms,(r,url,parma,header))
    
    print('已经发送短信验证码')
    smsinput=input('验证码:')
#     这里应该要做检查
    print('正在登陆，请稍后...')

    # 验证
    url='https://4acasp.gmcc.net/loginServlet.do?target=https://4a.gmcc.net/first.do?method=login&authType=noteAuth&appCode=IAM000'
    parma={'random_form':loginForm2,'loginPage':'/auth/nextUserLogin.jsp','userName':cn_name,'passWord':'','tokenName':cn_name,'isUsePin':'true','updatePin':'false','tokenpassword':'','pinCode':'','smsName':cn_name,'smsPwd':cn_pwd_saw,'dynamic_smsPwd':smsinput,'checkCodeTemp':'','figerName':'','challengeName':cn_name,'challegePassword':'','vpn':''}
    result=r.post(url,data=parma,headers=header,verify=False)

    #信息同步
    random2='0.'+str(random.randint(100000000000000,999999999999999))+str(random.randint(1,9))
    s=r.get('https://4a.gmcc.net/synAuthz.do?method=syn&rnd='+random2,headers=header,verify=False)
#     print s.text
    #-----{success:true,code:'null',text:'null'}---------

    #登陆4A
    random2='0.'+str(random.randint(100000000000000,999999999999999))+str(random.randint(1,9))
    r.get('https://4a.gmcc.net/main.jsp?rnd='+random2,headers=header,verify=False)
    r.get('https://4a.gmcc.net/SystemmsgPortlet.lp?id=systemmsg&userID='+'yychijianyi'+'&resType=1',headers=header)
    random2='0.'+str(random.randint(100000000000000,999999999999999))+str(random.randint(1,9))
    r.get('https://4a.gmcc.net/synAuthz.do?method=syn2AppServer&rnd='+random2,headers=header,verify=False)
    r.get('https://4a.gmcc.net/page/resgroup/searchFrame.jsp',headers=header,verify=False)
    r.post('https://4a.gmcc.net/keystore.do',data={'method':'getKeyStoreList'},headers=header,verify=False)
    #get:https://4a.gmcc.net/page/resource/appres/appresourceQuery.do?method=listIni
    r.post('https://4a.gmcc.net/page/resource/appres/appresourceQuery.do',data={'method':'pageQuery','_gt_json':'{"recordType":"object","pageInfo":{"pageSize":50,"pageNum":1,"totalRowNum":0,"totalPageNum":0,"startRowNum":0,"endRowNum":0},"columnInfo":[{"id":"id","header":"资源ID","fieldName":"id","fieldIndex":"id","sortOrder":null,"hidden":true,"exportable":true,"printable":true},{"id":"hasDueAcc","header":"hasDueAcc","fieldName":"hasDueAcc","fieldIndex":"hasDueAcc","sortOrder":null,"hidden":true,"exportable":true,"printable":true},{"id":"groupName","header":"资源组","fieldName":"groupName","fieldIndex":"groupName","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"name","header":"资源名称","fieldName":"name","fieldIndex":"name","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"ip","header":"IP地址","fieldName":"ip","fieldIndex":"ip","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"restype","header":"资源类型","fieldName":"restype","fieldIndex":"restype","sortOrder":null,"hidden":true,"exportable":true,"printable":true},{"id":"appResAccountList","header":"从帐号列表","fieldName":"id","fieldIndex":"id","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"ssoMode","header":"ssoMode","fieldName":"ssoMode","fieldIndex":"ssoMode","sortOrder":null,"hidden":"true","exportable":true,"printable":true},{"id":"sysResClientList","header":"登录","fieldName":"id","fieldIndex":"id","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"opt","header":"操作","fieldName":"id","fieldIndex":"id","sortOrder":null,"hidden":false,"exportable":true,"printable":true}],"sortInfo":[],"filterInfo":[],"parameters":{},"action":"load"}'},headers=header,verify=False)
    r.post('https://4a.gmcc.net/keystore.do',data={'method':'getKeyStoreList'},headers=header,verify=False)
           
    params2={'method':'pageQuery','_gt_json':'{"recordType":"object","pageInfo":{"totalRowNum":-1,"pageSize":50,"pageNum":1,"totalPageNum":0,"startRowNum":0,"endRowNum":0},"columnInfo":[{"id":"id","header":"资源ID","fieldName":"id","fieldIndex":"id","sortOrder":null,"hidden":true,"exportable":true,"printable":true},{"id":"hasDueAcc","header":"hasDueAcc","fieldName":"hasDueAcc","fieldIndex":"hasDueAcc","sortOrder":null,"hidden":true,"exportable":true,"printable":true},{"id":"groupName","header":"资源组","fieldName":"groupName","fieldIndex":"groupName","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"name","header":"资源名称","fieldName":"name","fieldIndex":"name","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"ip","header":"IP地址","fieldName":"ip","fieldIndex":"ip","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"restype","header":"资源类型","fieldName":"restype","fieldIndex":"restype","sortOrder":null,"hidden":true,"exportable":true,"printable":true},{"id":"appResAccountList","header":"从帐号列表","fieldName":"id","fieldIndex":"id","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"ssoMode","header":"ssoMode","fieldName":"ssoMode","fieldIndex":"ssoMode","sortOrder":null,"hidden":"true","exportable":true,"printable":true},{"id":"sysResClientList","header":"登录","fieldName":"id","fieldIndex":"id","sortOrder":null,"hidden":false,"exportable":true,"printable":true},{"id":"opt","header":"操作","fieldName":"id","fieldIndex":"id","sortOrder":null,"hidden":false,"exportable":true,"printable":true}],"sortInfo":[],"filterInfo":[],"parameters":{},"action":"load"}','queryName':'','queryIP':'','isQuerySubTree':'1'}
    result2=r.post('https://4a.gmcc.net/page/resource/appres/appresourceQuery.do',data=params2,headers=header,verify=False)
#     print result2.text
    json2=json.loads(result2.text)
    print(json2)
    return json2
    
       
def cn_json_load(json2,cn_system):
    cn_i=0
    for i in json2.get('data'):
        ss=i.get('name')
        if ss==cn_system:
            break
        cn_i=cn_i+1
    print(json2.get('data')[cn_i].get('appResAccountList'))
    appResAccountList=json2.get('data')[cn_i].get('appResAccountList').split('|')[0][:-1]
    id_num=json2.get('data')[cn_i].get('id')
    return [appResAccountList,id_num]
           
           
def cn_ESOPLogin(r,json2):
   
    header={'User-Agent':'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate'}
    #点击ESOP登陆
    cn_temp=cn_json_load(json2,u'广东移动NGESOP系统')
    appResAccountList=cn_temp[0]
    id_num=cn_temp[1]
#     print id_num
#     print appResAccountList

    #同步数据
    r.post('https://4a.gmcc.net/keystore.do',data={'method':'getKeyStoreList'},headers=header,verify=False)
    r.post('https://4a.gmcc.net/page/resource/resourceQuery.do?',data={'method':'isAuthDateValid','subaccName':'AGZGT0000829'},headers=header,verify=False)
    
    params2={'method':'checkPolicy4JK','resId':id_num,'resAccId':appResAccountList,'date':str(time.time()).replace('.','')+str(random.randint(1,9))}
    result2=r.post('https://4a.gmcc.net/page/jk/sso/appJKLogin.do',data=params2,headers=header,verify=False)
    
#     params2={'method':'queryLoginJKStatus','resId':id_num,'resAccId':appResAccountList,'date':str(time.time()).replace('.','')+str(random.randint(1,9))}
#     r.post('https://4a.gmcc.net/page/jk/sso/appJKLogin.do',data=params2,headers=header,verify=False)
    params2={'method':'wantGetMACAddress','resId':id_num}
    r.post('https://4a.gmcc.net/sso.do',data=params2,headers=header,verify=False)
    
    url2='https://4a.gmcc.net/sso.do?method=appssoData&accID='+appResAccountList+'&resID='+id_num+'&softname=webAppByIE&date='+str(time.time()).replace('.','')+str(random.randint(1,9))
    params2={'txtMACAddr':'08:00:27:10:3A:FB','txtIPAddr':'10.0.2.15','txtDNSName':'gzshizhongxia'}
    print('-----------测试是否登陆ESOP成功-----------')
    s=r.post(url2,data=params2,headers=header,allow_redirects=True,verify=False)
    print(s)
    
    

    
def cn_BossLogin(r,json2):
        
    cn_subaccName='AGZGT0000829'
    header={'user-agent':'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:42.0) Gecko/20100101 Firefox/42.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate'}
    header2={'user-agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; SE 2.X MetaSr 1.0)','Accept':'image/jpeg,application/x-ms-application,image/gif,application/xaml+xml,image/pjpeg,application/x-ms-xbap,*/*','Accept-Language':'zh-CN','Accept-Encoding':'gzip, deflate'}
    #点击BOSS登陆
    cn_temp=cn_json_load(json2,u'广州NGBOSS前台')
    appResAccountList=cn_temp[0]
    id_num=cn_temp[1]
#     print appResAccountList
#     print id_num
    
    #同步数据
    r.post('https://4a.gmcc.net/page/resource/resourceQuery.do',data={'method':'isAuthDateValid','subaccName':cn_subaccName,},headers=header,verify=False)
    params2={'method':'checkPolicy4JK','resId':id_num,'resAccId':appResAccountList,'date':str(time.time()).replace('.','')+str(random.randint(1,9))}
    r.post('https://4a.gmcc.net/page/jk/sso/appJKLogin.do',data=params2,headers=header,verify=False)
    params2={'method':'wantGetMACAddress','resId':id_num}
    r.post('https://4a.gmcc.net/sso.do',data=params2,headers=header,verify=False)
    
    s=r.get('https://4a.gmcc.net/page/portlet/resshow/macaddress.jsp?formUrl=/sso.do?method=appssoData&accID='+appResAccountList+'&resID='+id_num+'&softname=webAppByIE&date='+str(time.time()).replace('.','')+str(random.randint(1,9)),headers=header)
    
    url2='https://4a.gmcc.net/sso.do?method=appssoData&accID='+appResAccountList+'&resID='+id_num+'&softname=webAppByIE&date='+str(time.time()).replace('.','')+str(random.randint(1,9))
    params2={'txtMACAddr':'08:00:27:44:EC:99','txtIPAddr':'10.0.2.15','txtDNSName':'gzshizhongxia'}
    print('-----------测试是否登陆BOSS成功-----------')
    s1=r.post(url2,data=params2,headers=header2,allow_redirects=True,verify=False)
#     print s1.text
    s1=r.get('http://10.252.17.241/csp/mif/mainFrameForNG.action?showPlay=null',headers=header)
#     print s1