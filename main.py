import itchat
from itchat.content import TEXT
import threading
from process import CnMsgProcess
import platform
import requests
import process


class MyThread(threading.Thread):
    def __init__(self, thread_id, name, counter):
        threading.Thread.__init__(self)
        self.threadID = thread_id
        self.name = name
        self.counter = counter

    def run(self):
        while True:
            a = input()
            # print(a)
            b = a.split(' ')
            # print(b)
            if len(b) == 2:
                itchat.send(b[1], b[0])
            elif len(b) == 1:
                itchat.send(a)
            # 这里要继续补充


def main(self, _r):
    @itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True)
    # isGroupChat=True
    def simple_reply(msg):
        _from_username = msg.FromUserName
        _to_username = msg.ToUserName
        _text = msg.Text
        _response = self.cn_msg_process(msg)
        # 返回结果是一个 list
        # ['operate_ok', _from_username, _order_name, order_param]

        if _response is None:
            pass
        elif type(_response) == list:
            _deal_result = process.cn_cmcc_process(_r, _response[2], _response[3])
            # 办理结果

            if type(_deal_result) == tuple and _deal_result[0] == '4a_login_up':
                itchat.send('需要登陆4A，请回复验证码')
                itchat.send(_deal_result[1])
            elif _deal_result[0] == '4a_login_up_success':
                itchat.send('成功登陆4A')
                for _i in _deal_result[1].split(';'):
                    itchat.send(_i)
            elif _deal_result[0] == 'errer402':
                itchat.send(_deal_result[1])
            elif _deal_result[0] == 'iot_login_up':
                itchat.send('成功登陆iot系统')
        else:
            _at = ''
            if _from_username[0:2] == '@@':
                # 证明是群聊天

                _is_friend = itchat.search_friends(userName=msg.ActualUserName)
                # 返回None，或搜索结果

                if _is_friend is None:
                    _at = '@' + msg['ActualNickName'] + '\n'
                else:
                    _at = '@' + _is_friend.NickName + '\n'
            _temp_status = 0
            for _i in _response.split('@|@'):
                if _temp_status == 0:
                    _temp_status = 1
                    itchat.send(_at + _i, toUserName=_from_username)
                else:
                    itchat.send(_i, toUserName=_from_username)
        # a.setdefault('chinafishz',{'ordername':'#puk','param':{}}).setdefault('param',{'c':3,'b':2}).update({'c':3,'b':2})
        # if(msg.FromUserName!='@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d'):
        #     print('【接收】'+msg.User.RemarkName+':'+msg.Text,msg.FromUserName)
        # elif(msg.FromUserName=='@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d'):
        #     if(msg.ToUserName=='@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d'):
        #         print('【自己】' + msg.Text, msg.FromUserName)
        #     else:
        #         print('【发给】'+msg.User.RemarkName+':'+msg.Text,msg.ToUserName)

    if platform.machine() != 'aarch64':
        itchat.auto_login(hotReload=True)
    else:
        itchat.auto_login(hotReload=True, enableCmdQR=2)

    itchat.run()


thread1 = MyThread(1, 'thread-1', 1)
thread1.start()


cn_order_list = {}
cn_chart_list = {}
# cn_order_list表示待办理的命令
# cn_chart_list表示待回复的对话

r = requests.session()
cn_msg_process = CnMsgProcess(cn_order_list, cn_chart_list)
# def __init__(self, msg, cn_order_list, cn_chart_list)

main(cn_msg_process, r)
