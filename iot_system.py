
# -*-encoding:utf-8-*-
import socket
import time
import random
from bs4 import BeautifulSoup
from requests.auth import HTTPProxyAuth
import cn_system


def test_alive(_r, _proxies, _auth):
    # url = ''
    # s = self.r.get(url, auth=self.auth, proxies=self.proxies)
    try:
        iot_status(_r, '17228107947', _proxies, _auth)
        return 'alive'
    except:
        return 'not alive'


def iot_status(_r, phone_num, _proxies, _auth):
    header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E)',
              'Accept': '*/*', 'Accept-Language': 'zh-CN', 'Accept-Encoding': 'gzip, deflate'}

    _random = '0.'+str(random.randint(100000000000000,999999999999999))+str(random.randint(1,9))
    url = 'http://10.253.61.8/ngcustcare/chargesrv/common/qryRelateSubs.action?servNumber=' + phone_num + '&isSupportGrp=undefined&random='+_random
    s = _r.get(url, headers=header, auth=_auth, proxies=_proxies)
    soup = BeautifulSoup(s.text, 'lxml')
    _result = ''.join(soup.select('#columnDiv1')[0].find(attrs={"name":"subscriber_tr"}).select('td')[3].text).split()[0]
    return _result


def iot_phone_query_base(r, phone_num, _proxies, _auth):
    def cn_cookies(cookies_temp):
        cookies = dict()
        for i in r.cookies.get_dict('10.253.61.8'):
            cookies[i] = r.cookies.get(i, '', '10.253.61.8')
        cookies['bsacKF'] = 'NGCRM_BOSS'
        cookies['com.huawei.boss.CONTACTID'] = 'null'
        cookies['com.huawei.boss.CURRENT_MENUID'] = 'null'
        cookies['com.huawei.boss.CURRENT_TAB'] = 'cvalida'
        cookies['com.huawei.boss.CURRENT_USER'] = 'com.huawei.boss.NO_CURRENT_USER'
        return cookies

    def cn_cookies2(cookies, phone_num):
        cookies = dict()
        for i in r.cookies.get_dict('10.253.61.8'):
            cookies[i] = r.cookies.get(i, '', '10.253.61.8')
        cookies['bsacKF'] = 'NGCRM_BOSS'
        cookies['com.huawei.boss.CONTACTID'] = 'undefined'
        cookies['com.huawei.boss.CURRENT_MENUID'] = '100110121062'
        cookies['com.huawei.boss.CURRENT_TAB'] = 'BOSS%5E' + phone_num + '%5E100110121062%7E' + phone_num
        cookies['com.huawei.boss.CURRENT_USER'] = phone_num
        cookies['MACAddr'] = 'null'
        cookies['sDNSName'] = '3B8MB8'
        return cookies

    def cn_soup(temp):
        a = soup.find(attrs={"name": temp}).attrs['value']
        return a

    header2 = {
        'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0; SE 2.X MetaSr 1.0)',
        'Accept': '*/*', 'Accept-Language': 'zh-cn', 'Accept-Encoding': 'gzip, deflate',
        'X-Requested-With': 'XMLHttpRequest'}

    cookies1 = cn_cookies(r.cookies)
    url = 'http://10.253.61.8/ngcustcare/custlogin/qryCustInfo.action'
    parma = {'method': 'qryCustInfo', 'servNumber': phone_num, 'authCheckMode': 'AuthCheckZ', 'verifyCode': '',
             'pswd': '', 'certType': 'IdCard', 'certID': '', 'rndPswd': '', 'custType': 'PersonCustomer',
             'domainType': 'null', 'isCert2G': '', 'ONLYLOGIN': 'onlyLogin', 'withoutPassValidate': 'true',
             'isUseReadIdCardWithTwo': '0'}
    s = r.post(url, cookies=cookies1, data=parma, headers=header2, auth=_auth, proxies=_proxies)

    cn_cookies = cn_cookies2(r.cookies, phone_num)
    url2 = 'http://10.253.61.8/ngcustcare/uniteview/uviewtwo/uvDisper.action?currentTabID=BOSS^' + phone_num + '^100110121062~' + phone_num
    s2 = r.get(url2, cookies=cn_cookies, headers=header2, auth=_auth, proxies=_proxies)
    soup = BeautifulSoup(s2.text, 'lxml')

    cn_cookies3 = cn_cookies2(r.cookies, phone_num)
    url3 = 'http://10.253.61.8/nguniteview/bossviewhome.jsp'
    parma3 = {'ccm_ObjectID': '', 'ccm_RandomNum': '', 'ccdirect': soup.find(attrs={"name": "ccdirect"}).attrs['value'],
              'ccm_EntityID': soup.find(attrs={"name": "ccm_EntityID"}).attrs['value'],
              'ccm_EntityName': soup.find(attrs={"name": "ccm_EntityName"}).attrs['value'],
              'ccm_CreateDate': soup.find(attrs={"name": "ccm_CreateDate"}).attrs['value'],
              'ccm_Status': soup.find(attrs={"name": "ccm_Status"}).attrs['value'],
              'ccm_StatusDate': soup.find(attrs={"name": "ccm_StatusDate"}).attrs['value'],
              'ccm_EditStatus': soup.find(attrs={"name": "ccm_EditStatus"}).attrs['value'], 'ccm_Region': '200',
              'ccm_ShortName': '', 'ccm_Password': soup.find(attrs={"name": "ccm_Password"}).attrs['value'],
              'ccm_CustType': 'PersonCustomer', 'ccm_VipType': soup.find(attrs={"name": "ccm_VipType"}).attrs['value'],
              'ccm_Foreigner': soup.find(attrs={"name": "ccm_Foreigner"}).attrs['value'],
              'ccm_CustClass1': soup.find(attrs={"name": "ccm_CustClass1"}).attrs['value'],
              'ccm_CustClass2': soup.find(attrs={"name": "ccm_CustClass2"}).attrs['value'],
              'ccm_National': soup.find(attrs={"name": "ccm_National"}).attrs['value'], 'ccm_Address': '********',
              'ccm_CertID': soup.find(attrs={"name": "ccm_CertID"}).attrs['value'],
              'ccm_CertType': soup.find(attrs={"name": "ccm_CertType"}).attrs['value'], 'ccm_CertAddr': '********',
              'ccm_LinkMan': soup.find(attrs={"name": "ccm_LinkMan"}).attrs['value'],
              'ccm_LinkPhone': soup.find(attrs={"name": "ccm_LinkPhone"}).attrs['value'], 'ccm_HomeTel': '',
              'ccm_OfficeTel': '', 'ccm_MobileTel': '',
              'ccm_PostCode': soup.find(attrs={"name": "ccm_PostCode"}).attrs['value'], 'ccm_LinkAddr': '********',
              'ccm_Email': '', 'ccm_HomePage': '', 'ccm_IsMergeBill': '1',
              'ccm_CreditLevel': soup.find(attrs={"name": "ccm_CreditLevel"}).attrs['value'],
              'ccm_OwnerAreaID': soup.find(attrs={"name": "ccm_OwnerAreaID"}).attrs['value'],
              'ccm_OrgID': soup.find(attrs={"name": "ccm_OrgID"}).attrs['value'], 'ccm_RegStatus': '1',
              'ccm_Notes': soup.find(attrs={"name": "ccm_Notes"}).attrs['value'], 'ccm_ResponseCustMgr': '',
              'ccm_CurrentCustMgr': '', 'ccm_InLevel': soup.find(attrs={"name": "ccm_InLevel"}).attrs['value'],
              'ccm_TownID': '',
              'ccm_VipTypeStateDate': soup.find(attrs={"name": "ccm_VipTypeStateDate"}).attrs['value'],
              'ccm_NetServGrade': '', 'ccm_CustAddrArray': '[]', 'ccm_CustBillArray': '[]', 'ccm_IsEncrypt': '1',
              'ccm_starLevel': soup.find(attrs={"name": "ccm_starLevel"}).attrs['value'],
              'ccm_IsFaceChk': soup.find(attrs={"name": "ccm_IsFaceChk"}).attrs['value'],
              'ccregister': soup.find(attrs={"name": "ccregister"}).attrs['value'],
              'ccnotRegister': soup.find(attrs={"name": "ccnotRegister"}).attrs['value'], 'csm_ObjectID': '',
              'csm_RandomNum': '', 'csdirect': soup.find(attrs={"name": "csdirect"}).attrs['value'],
              'csm_EntityID': soup.find(attrs={"name": "csm_EntityID"}).attrs['value'],
              'csm_EntityName': cn_soup('csm_EntityName'), 'csm_CreateDate': cn_soup('csm_CreateDate'),
              'csm_Status': cn_soup('csm_Status'), 'csm_StatusDate': '******',
              'csm_EditStatus': cn_soup('csm_EditStatus'), 'csm_Region': '200', 'csm_Password': cn_soup('csm_Password'),
              'csm_ProductID': cn_soup('csm_ProductID'), 'csm_ServNumber': cn_soup('csm_ServNumber'),
              'csm_RegisterOrgID': cn_soup('csm_RegisterOrgID'), 'csm_OwnerOrgID': cn_soup('csm_OwnerOrgID'),
              'csm_AccountOid': cn_soup('csm_AccountOid'), 'csm_CustomerOid': cn_soup('csm_CustomerOid'),
              'csm_AuthType': 'AuthCheckB', 'csm_MobileType': 'mbtpNml', 'csm_AreaID': '', 'csm_PayMode': '1',
              'csm_StopKey': cn_soup('csm_StopKey'), 'csm_Brand': cn_soup('csm_Brand'),
              'csm_StartDate': cn_soup('csm_StartDate'), 'csm_InvalidDate': cn_soup('csm_InvalidDate'),
              'csm_SettleDay': '1', 'csm_Enum': cn_soup('csm_Enum'), 'csm_Imsi': cn_soup('csm_Imsi'), 'csm_Credit': '0',
              'csm_SubsProduct': '[]', 'csm_IsDefaultTelNum': '1', 'csm_BelongRegion': '0', 'csm_TargetRegion': '0',
              'csm_CretLevel': '', 'csgotone': cn_soup('csgotone'), 'csnotGotone': cn_soup('csnotGotone'),
              'cam_ObjectID': '', 'cam_RandomNum': '', 'cadirect': cn_soup('cadirect'),
              'cam_EntityID': cn_soup('cam_EntityID'), 'cam_EntityName': cn_soup('cam_EntityName'),
              'cam_CreateDate': cn_soup('cam_CreateDate'), 'cam_Status': cn_soup('cam_Status'),
              'cam_StatusDate': cn_soup('cam_StatusDate'), 'cam_EditStatus': '0', 'cam_Region': '200',
              'cam_CustID': cn_soup('cam_CustID'), 'cam_GroupAcctID': '', 'cam_PrePayType': 'pptpPost',
              'cam_AccountType': 'actpCmn', 'cam_OverDraft': '0', 'cam_ControlScheme': '0',
              'cam_EntrustTel': cn_soup('cam_EntrustTel'), 'cam_OrgID': cn_soup('cam_OrgID'), 'cam_NotifyType': '0',
              'cam_NotifyValue': '0', 'cam_InvPrintType': 'InvPTbillfee', 'cam_Notes': '', 'cam_PayChannelArray': '[]',
              'cam_CustBillArray': '[]', 'cam_UrgeInfos': '[]', 'cam_SettleAccount': '', 'cam_IsDefault': '1',
              'cam_BillInvoiceMailArray': '[]', 'cam_NotifyValueDisplay': '0',
              'cam_CreateDateDisplay': cn_soup('cam_CreateDateDisplay'), 'com_ObjectID': '', 'com_RandomNum': '',
              'comenuId': cn_soup('comenuId'), 'codirect': 'FALSE', 'com_EntityID': 'AGZGT0000829',
              'com_EntityName': cn_soup('com_EntityName'), 'com_CreateDate': cn_soup('com_CreateDate'),
              'com_Status': cn_soup('com_Status'), 'com_StatusDate': cn_soup('com_StatusDate'), 'com_EditStatus': '0',
              'com_Region': '200', 'coerrorInfoForControl': '', 'conodeID': 'AGZGT0000829',
              'conodeName': cn_soup('conodeName'), 'conodeParentID': cn_soup('conodeParentID'),
              'coentityID': 'AGZGT0000829', 'cootherParam': cn_soup('cootherParam'), 'cochecked': cn_soup('cochecked'),
              'com_MenuID': cn_soup('com_MenuID'), 'com_ServNum': '', 'com_TouchNum': '',
              'com_Password': cn_soup('com_Password'), 'com_OrgID': cn_soup('com_OrgID'), 'com_RoamOrgID': '',
              'com_PassChangeDate': cn_soup('com_PassChangeDate'), 'com_OperType': cn_soup('com_OperType'),
              'com_Manager': '0', 'com_Level': '', 'com_ContactPhone': '13922204911',
              'com_MacAddress': cn_soup('com_MacAddress'), 'com_OnDuty': '0', 'com_ShareStore': '', 'com_BirthDay': '',
              'com_WorkDate': '', 'com_CertID': '', 'com_Sex': '', 'com_EducationLevel': '', 'com_TotalLevel': '',
              'com_SkillLevel': '', 'com_TrainLevel': '', 'com_ComityLevel': '', 'com_Operator_type': '0',
              'com_NativeHome': '', 'com_graduateDate': '', 'com_IsMarray': '0', 'com_PolityFace': '',
              'com_HomeAddress': '', 'com_JobLive': '', 'com_NowPostID': '', 'com_BloodType': '', 'com_Healthy': '',
              'com_Character': '', 'com_Enjoyful': '', 'com_PriSocietyRelation': '', 'com_FamilyDes': '',
              'com_StarLevel': '', 'com_AssessRec': '', 'com_hr_status': '1', 'com_Restrict_time': '0',
              'com_Start_time': '0', 'com_End_time': '24', 'com_Enable_gprs': '0', 'com_Gprs_starttime': '0',
              'com_Gprs_endtime': '0', 'com_Check_mac': '0', 'com_Mac': '', 'com_IPAddress': '10.244.110.143',
              'costartUsingTime': cn_soup('costartUsingTime'), 'coendUsingTime': cn_soup('coendUsingTime'),
              'com_QueueID': '', 'com_InvVersion': '', 'com_areaID': '', 'servNumber': cn_soup('servNumber'),
              'transmit': cn_soup('transmit'), 'recType': '', 'stopKeyValue': cn_soup('stopKeyValue'),
              'remotemac': '08-00-27-44-EC-99'}
    s = r.post(url3, data=parma3, cookies=cn_cookies3, headers=header2, auth=_auth, proxies=_proxies)
    return s.text


def iot_puk(r,  _proxies, _auth):
    url = 'http://10.253.61.8/nguniteview/layoutAction.do?method=showView&ownerType=1&viewId=314'
    param = {'width': 767, 'height': '14'}
    s = r.post(url, data=param, auth=_auth, proxies=_proxies)
    soup = BeautifulSoup(s.text, 'lxml')
    _result = soup.select('td')[3].text
    return _result















