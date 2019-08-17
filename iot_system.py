
# -*-encoding:utf-8-*-
import socket
import time
import random
from bs4 import BeautifulSoup
from requests.auth import HTTPProxyAuth
import cn_system


def test_alive(_r):
    url = ''
    # s = self.r.get(url, auth=self.auth, proxies=self.proxies)
    try:
        iot_status('17128126857')
        return 'alive'
    except:
        return 'not alive'


def iot_status(_r, phone_num, _proxies, _auth):
    _random = '0.'+str(random.randint(100000000000000,999999999999999))+str(random.randint(1,9))
    url = 'http://10.253.61.8/ngcustcare/chargesrv/common/qryRelateSubs.action?servNumber=' + phone_num + '&isSupportGrp=undefined&random='+_random
    s = _r.get(url, auth=_auth, proxies=_proxies)
    soup = BeautifulSoup(s.text, 'lxml')
    return ''.join(soup.select('#columnDiv1')[0].find(attrs={"name":"subscriber_tr"}).select('td')[3].text).split()[0]


















