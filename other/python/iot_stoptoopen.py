#-*-encoding:utf-8-*-

# 操作停开机

import time
import random
from bs4  import BeautifulSoup

def cn_iot_qianfeikaiji(r,cn_phone):
    def cn_cookies(cookies_temp):
            cookies = dict()
            for i in r.cookies.get_dict('10.253.61.8'):
                cookies[i]=r.cookies.get(i,'','10.253.61.8')
            cookies['bsacKF']='NGCRM_BOSS'
            cookies['com.huawei.boss.CONTACTID']='null'
            cookies['com.huawei.boss.CURRENT_MENUID']='null'
            cookies['com.huawei.boss.CURRENT_TAB']='cvalida'
            cookies['com.huawei.boss.CURRENT_USER']='com.huawei.boss.NO_CURRENT_USER'
#             cookies['GZCOMM']='r_GZ_CRM_WEB1_1082'
#             cookies['GZCRM']='r_GZ_CRM_WEB2_1081'
            return cookies

    def cn_cookies2(cookies,cn_phoneNum):
        cookies = dict()
        for i in r.cookies.get_dict('10.253.61.8'):
            cookies[i]=r.cookies.get(i,'','10.253.61.8')
        cookies['bsacKF']='NGCRM_BOSS'
        cookies['com.huawei.boss.CONTACTID']='undefined'
        cookies['com.huawei.boss.CURRENT_MENUID']='100110121062'
        cookies['com.huawei.boss.CURRENT_TAB']='BOSS%5E'+cn_phoneNum+'%5E100110121062%7E'+cn_phoneNum
        cookies['com.huawei.boss.CURRENT_USER']=cn_phoneNum
#         cookies['GZCOMM']='r_GZ_CRM_WEB1_1082'
#         cookies['GZCRM']='r_GZ_CRM_WEB2_1081'
        cookies['MACAddr']='null'
        cookies['sDNSName']='3B8MB8'
        return cookies
    
    def cn_soup(temp):
        a=soup.find(attrs={"name":temp}).attrs['value']
        return a

    header={'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; SE 2.X MetaSr 1.0)','Accept':'*/*','Accept-Language':'zh-cn','Accept-Encoding':'gzip, deflate'}
    header2={'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; SE 2.X MetaSr 1.0)','Accept':'*/*','Accept-Language':'zh-cn','Accept-Encoding':'gzip, deflate','X-Requested-With':'XMLHttpRequest'}
    header3={'User-Agent':'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; SE 2.X MetaSr 1.0)','Accept':'image/jpeg,application/x-ms-application,image/gif,application/xaml+xml,image/pjpeg, application/x-ms-xbap','Accept-Language':'zh-CN','Accept-Encoding':'gzip, deflate'}

    cookies1=cn_cookies(r.cookies)
    url='http://10.253.61.8/ngcustcare/custlogin/qryCustInfo.action'
    parma={'method':'qryCustInfo','servNumber':cn_phone,'authCheckMode':'AuthCheckZ','verifyCode':'','pswd':'','certType':'IdCard','certID':'','rndPswd':'','custType':'PersonCustomer','domainType':'null','isCert2G':'','ONLYLOGIN':'onlyLogin','withoutPassValidate':'true','isUseReadIdCardWithTwo':'0'}
    s=r.post(url,cookies=cookies1,data=parma,headers=header2)


    cn_cookies=cn_cookies2(r.cookies,cn_phone)
    url2='http://10.253.61.8/ngcustcare/uniteview/uviewtwo/uvDisper.action?currentTabID=BOSS^'+cn_phone+'^100110121062~'+cn_phone
    s2=r.get(url2,cookies=cn_cookies,headers=header2)
    soup=BeautifulSoup(s2.text,'lxml')

    cn_cookies3=cn_cookies2(r.cookies,cn_phone)
    url3='http://10.253.61.8/nguniteview/bossviewhome.jsp'
    parma3={'ccm_ObjectID':'','ccm_RandomNum':'','ccdirect':soup.find(attrs={"name":"ccdirect"}).attrs['value'],'ccm_EntityID':soup.find(attrs={"name":"ccm_EntityID"}).attrs['value'],'ccm_EntityName':soup.find(attrs={"name":"ccm_EntityName"}).attrs['value'],'ccm_CreateDate':soup.find(attrs={"name":"ccm_CreateDate"}).attrs['value'],'ccm_Status':soup.find(attrs={"name":"ccm_Status"}).attrs['value'],'ccm_StatusDate':soup.find(attrs={"name":"ccm_StatusDate"}).attrs['value'],'ccm_EditStatus':soup.find(attrs={"name":"ccm_EditStatus"}).attrs['value'],'ccm_Region':'200','ccm_ShortName':'','ccm_Password':soup.find(attrs={"name":"ccm_Password"}).attrs['value'],'ccm_CustType':'PersonCustomer','ccm_VipType':soup.find(attrs={"name":"ccm_VipType"}).attrs['value'],'ccm_Foreigner':soup.find(attrs={"name":"ccm_Foreigner"}).attrs['value'],'ccm_CustClass1':soup.find(attrs={"name":"ccm_CustClass1"}).attrs['value'],'ccm_CustClass2':soup.find(attrs={"name":"ccm_CustClass2"}).attrs['value'],'ccm_National':soup.find(attrs={"name":"ccm_National"}).attrs['value'],'ccm_Address':'********','ccm_CertID':soup.find(attrs={"name":"ccm_CertID"}).attrs['value'],'ccm_CertType':soup.find(attrs={"name":"ccm_CertType"}).attrs['value'],'ccm_CertAddr':'********','ccm_LinkMan':soup.find(attrs={"name":"ccm_LinkMan"}).attrs['value'],'ccm_LinkPhone':soup.find(attrs={"name":"ccm_LinkPhone"}).attrs['value'],'ccm_HomeTel':'','ccm_OfficeTel':'','ccm_MobileTel':'','ccm_PostCode':soup.find(attrs={"name":"ccm_PostCode"}).attrs['value'],'ccm_LinkAddr':'********','ccm_Email':'','ccm_HomePage':'','ccm_IsMergeBill':'1','ccm_CreditLevel':soup.find(attrs={"name":"ccm_CreditLevel"}).attrs['value'],'ccm_OwnerAreaID':soup.find(attrs={"name":"ccm_OwnerAreaID"}).attrs['value'],'ccm_OrgID':soup.find(attrs={"name":"ccm_OrgID"}).attrs['value'],'ccm_RegStatus':'1','ccm_Notes':soup.find(attrs={"name":"ccm_Notes"}).attrs['value'],'ccm_ResponseCustMgr':'','ccm_CurrentCustMgr':'','ccm_InLevel':soup.find(attrs={"name":"ccm_InLevel"}).attrs['value'],'ccm_TownID':'','ccm_VipTypeStateDate':soup.find(attrs={"name":"ccm_VipTypeStateDate"}).attrs['value'],'ccm_NetServGrade':'','ccm_CustAddrArray':'[]','ccm_CustBillArray':'[]','ccm_IsEncrypt':'1','ccm_starLevel':soup.find(attrs={"name":"ccm_starLevel"}).attrs['value'],'ccm_IsFaceChk':soup.find(attrs={"name":"ccm_IsFaceChk"}).attrs['value'],'ccregister':soup.find(attrs={"name":"ccregister"}).attrs['value'],'ccnotRegister':soup.find(attrs={"name":"ccnotRegister"}).attrs['value'],'csm_ObjectID':'','csm_RandomNum':'','csdirect':soup.find(attrs={"name":"csdirect"}).attrs['value'],'csm_EntityID':soup.find(attrs={"name":"csm_EntityID"}).attrs['value'],'csm_EntityName':cn_soup('csm_EntityName'),'csm_CreateDate':cn_soup('csm_CreateDate'),'csm_Status':cn_soup('csm_Status'),'csm_StatusDate':'******','csm_EditStatus':cn_soup('csm_EditStatus'),'csm_Region':'200','csm_Password':cn_soup('csm_Password'),'csm_ProductID':cn_soup('csm_ProductID'),'csm_ServNumber':cn_soup('csm_ServNumber'),'csm_RegisterOrgID':cn_soup('csm_RegisterOrgID'),'csm_OwnerOrgID':cn_soup('csm_OwnerOrgID'),'csm_AccountOid':cn_soup('csm_AccountOid'),'csm_CustomerOid':cn_soup('csm_CustomerOid'),'csm_AuthType':'AuthCheckB','csm_MobileType':'mbtpNml','csm_AreaID':'','csm_PayMode':'1','csm_StopKey':cn_soup('csm_StopKey'),'csm_Brand':cn_soup('csm_Brand'),'csm_StartDate':cn_soup('csm_StartDate'),'csm_InvalidDate':cn_soup('csm_InvalidDate'),'csm_SettleDay':'1','csm_Enum':cn_soup('csm_Enum'),'csm_Imsi':cn_soup('csm_Imsi'),'csm_Credit':'0','csm_SubsProduct':'[]','csm_IsDefaultTelNum':'1','csm_BelongRegion':'0','csm_TargetRegion':'0','csm_CretLevel':'','csgotone':cn_soup('csgotone'),'csnotGotone':cn_soup('csnotGotone'),'cam_ObjectID':'','cam_RandomNum':'','cadirect':cn_soup('cadirect'),'cam_EntityID':cn_soup('cam_EntityID'),'cam_EntityName':cn_soup('cam_EntityName'),'cam_CreateDate':cn_soup('cam_CreateDate'),'cam_Status':cn_soup('cam_Status'),'cam_StatusDate':cn_soup('cam_StatusDate'),'cam_EditStatus':'0','cam_Region':'200','cam_CustID':cn_soup('cam_CustID'),'cam_GroupAcctID':'','cam_PrePayType':'pptpPost','cam_AccountType':'actpCmn','cam_OverDraft':'0','cam_ControlScheme':'0','cam_EntrustTel':cn_soup('cam_EntrustTel'),'cam_OrgID':cn_soup('cam_OrgID'),'cam_NotifyType':'0','cam_NotifyValue':'0','cam_InvPrintType':'InvPTbillfee','cam_Notes':'','cam_PayChannelArray':'[]','cam_CustBillArray':'[]','cam_UrgeInfos':'[]','cam_SettleAccount':'','cam_IsDefault':'1','cam_BillInvoiceMailArray':'[]','cam_NotifyValueDisplay':'0','cam_CreateDateDisplay':cn_soup('cam_CreateDateDisplay'),'com_ObjectID':'','com_RandomNum':'','comenuId':cn_soup('comenuId'),'codirect':'FALSE','com_EntityID':'AGZGT0000829','com_EntityName':cn_soup('com_EntityName'),'com_CreateDate':cn_soup('com_CreateDate'),'com_Status':cn_soup('com_Status'),'com_StatusDate':cn_soup('com_StatusDate'),'com_EditStatus':'0','com_Region':'200','coerrorInfoForControl':'','conodeID':'AGZGT0000829','conodeName':cn_soup('conodeName'),'conodeParentID':cn_soup('conodeParentID'),'coentityID':'AGZGT0000829','cootherParam':cn_soup('cootherParam'),'cochecked':cn_soup('cochecked'),'com_MenuID':cn_soup('com_MenuID'),'com_ServNum':'','com_TouchNum':'','com_Password':cn_soup('com_Password'),'com_OrgID':cn_soup('com_OrgID'),'com_RoamOrgID':'','com_PassChangeDate':cn_soup('com_PassChangeDate'),'com_OperType':cn_soup('com_OperType'),'com_Manager':'0','com_Level':'','com_ContactPhone':'13922204911','com_MacAddress':cn_soup('com_MacAddress'),'com_OnDuty':'0','com_ShareStore':'','com_BirthDay':'','com_WorkDate':'','com_CertID':'','com_Sex':'','com_EducationLevel':'','com_TotalLevel':'','com_SkillLevel':'','com_TrainLevel':'','com_ComityLevel':'','com_Operator_type':'0','com_NativeHome':'','com_graduateDate':'','com_IsMarray':'0','com_PolityFace':'','com_HomeAddress':'','com_JobLive':'','com_NowPostID':'','com_BloodType':'','com_Healthy':'','com_Character':'','com_Enjoyful':'','com_PriSocietyRelation':'','com_FamilyDes':'','com_StarLevel':'','com_AssessRec':'','com_hr_status':'1','com_Restrict_time':'0','com_Start_time':'0','com_End_time':'24','com_Enable_gprs':'0','com_Gprs_starttime':'0','com_Gprs_endtime':'0','com_Check_mac':'0','com_Mac':'','com_IPAddress':'10.244.110.143','costartUsingTime':cn_soup('costartUsingTime'),'coendUsingTime':cn_soup('coendUsingTime'),'com_QueueID':'','com_InvVersion':'','com_areaID':'','servNumber':cn_soup('servNumber'),'transmit':cn_soup('transmit'),'recType':'','stopKeyValue':cn_soup('stopKeyValue'),'remotemac':'08-00-27-44-EC-99'}
    s3=r.post(url3,data=parma3,cookies=cn_cookies3,headers=header2)


    url='http://10.253.61.8/ngcustcare/common/submits/unitCommonSubmit.action?flow=productOrientedFlow&version=1.01'
    result=r.get(url,headers=header2)
    soup=BeautifulSoup(result.text,'lxml')
    s=soup.find(attrs={"name":"submits/unitCommonSubmit"}).attrs['value']



    url='http://10.253.61.8/ngcustcare/custsvc/stopopen/stopOpenCommit.action'
    param={"stopOpenType":"30000000","stopOpenReason":"NotReg","stopOpenMemo":"非实名停机","hiddenTokenName":"submits/unitCommonSubmit","submits/unitCommonSubmit":s}
    result=r.post(url,data=param,headers=header2,cookies=cn_cookies3)
    cn_hiddenTokenName_value=BeautifulSoup(result.text,'lxml').find(attrs={"name":"fee/calculate"}).attrs['value']
    # print(cn_hiddenTokenName_value)

    parmas={"PreBussOrderId":"","withdrawGoods":"","payTypeBean.cashAmt":"","payTypeBean.chequeAmt":"","payTypeBean.bankId":"","payTypeBean.bankName":"","payTypeBean.chequeNum":"","payTypeBean.cardAmt":"","payTypeBean.posNum":"","payTypeBean.confirmPosNum":"","payTypeBean.weiXinPayAmt":"","payTypeBean.weiXinPayNum":"","payTypeBean.aliPayAmt":"","payTypeBean.orderId":"","payTypeBean.aliPayPayNum":"","payTypeBean.newSeparatePayAmt":"","payTypeBean.acctCash":"","payTypeBean.orderId":"","payTypeBean.newSeparatePayNum":"","payTypeBean.preAuthSeparatePayAmt":"","payTypeBean.orderId":"","payTypeBean.preAuthSeparatePayNum":"","payTypeBean.acctCash":"","payTypeBean.acctId":"-1","payTypeBean.acctPayCash":"","payTypeBean.acctPayId":"-1","payTypeBean.scoreCash":"","payTypeBean.score":"","payTypeBean.scoreTransRule":"1/1","payTypeBean.m":"0","payTypeBean.mTransRule":"1/1","payTypeBean.bankAmt":"","payTypeBean.posautocardAmt":"","payTypeBean.posautocardNum":"","payTypeBean.posautoTerminalno":"","payTypeBean.posautoReferno":"","payTypeBean.posautoMerchantno":"","payTypeBean.posnotautoAmt":"","payTypeBean.posnotautocardNum":"","payTypeBean.posnotautoTerminalno":"","payTypeBean.posnotautoReferno":"","payTypeBean.posnotautoMerchantno":"","payTypeBean.separateAmt":"","payTypeBean.separateBankId":"GH","payTypeBean.separateBankName":"工行","payTypeBean.separateBankAcct":"","payTypeBean.separateBankUserName":"","payTypeBean.separatePosNum":"","payTypeBean.limitCash":"","payTypeBean.unlimitCash":"","BARGAINFEEXML":"","CHANGEFEEBYBARGAINXML":"@260@263xml@232version@261@2341@2460@234@232encoding@261@234UTF@2458@234@263@262@260huawei@295call@262@260i@262common@247fee@247@242@260@247i@262@260e@262changeFeeByBargain@260@247e@262@260p@262@260m@262@260n@2620@260@247n@262@260t@262a@260@247t@262@260v@262@260@247v@262@260@247m@262@260m@262@260n@2621@260@247n@262@260t@262a@260@247t@262@260v@262@260@247v@262@260@247m@262@260@247p@262@260@247huawei@295call@262","UPDATEPAYTYPEBYPAGEDATAXML":"@260@263xml@232version@261@2341@2460@234@232encoding@261@234UTF@2458@234@263@262@260huawei@295call@262@260i@262common@247fee@247@242@260@247i@262@260e@262updatePayTypeByPageData@260@247e@262@260p@262@260m@262@260n@2620@260@247n@262@260t@262a@260@247t@262@260v@262@260@247v@262@260@247m@262@260@247p@262@260@247huawei@295call@262","reccustinfo_name":"","reccustinfo_phone":"","reccustinfo_certificateType":"IdCard","reccustinfo_certificateNum":"440103198607251838","reccustinfo_address":"","emergencyContactNo":"","reccustinfo_note":"","invoicePrintMode":"","hiddenTokenName":"fee/calculate","fee/calculate":cn_hiddenTokenName_value,"receiptNumber":"00000000","invoiceType":"1","assembleInvoice":"0","invoiceNumber":"00000000"}
    s=r.post('http://10.253.61.8/ngcustcare/common/fee/pay.action',data=parmas,headers=header3,cookies=cn_cookies3)
    s=BeautifulSoup(s.text,'lxml').select('.title_boldtext')[0].text

    time.sleep(1)

    # 清理
    parmas={}
    r.post('http://10.253.61.8/ngcustcare/clearUserSession.do?tabid=BOSS^'+cn_phone+'^ServiceOnStopOrStart~'+cn_phone,data=parmas)
    r.post('http://10.253.61.8/ngcustcare/clearUserSession.do?tabid=BOSS^'+cn_phone+'^100110121062~'+cn_phone,data=parmas)

    return s


