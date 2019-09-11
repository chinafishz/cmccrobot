import itchat
from itchat.content import TEXT
import threading
from process import CnMsgProcess
import platform
import requests
import process
import importlib as imp

def main(self):
    @itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True)
    def simple_reply(msg):
        _from_username = msg.FromUserName
        _to_username = msg.ToUserName
        _text = msg.Text
        _response = self.cn_msg_process(msg)
        # 返回结果是一个 list
        # ['operate_ok', _from_username, _order_name, order_param]

        while True:
            # while：目的是当系统登陆前一些待办命令需要在系统登陆后马上处理

            _deal_result = self.cmcc_process(_response)
            # 返回的结果是一个tuple
            if _deal_result is None:
                break
            elif _deal_result[0] == '4a_login_up':
                itchat.send('需要登陆4A，请回复验证码')
                itchat.send(_deal_result[1])
                itchat.send('后台没有登陆系统，等待管理员操作，完成后将自动回复指令，请稍等~', toUserName=_from_username)
            elif _deal_result[0] == '4a_login_up_success':
                itchat.send('成功登陆4A')
                for _i in _deal_result[1].split(';'):
                    if _i.split('|')[0] in ['广东移动NGESOP系统','广州NGBOSS前台','物联网系统前台']:
                        itchat.send(_i)
            elif _deal_result[0] == 'iot_login_up':
                itchat.send('成功登陆iot系统')
                self.config_list['iot_todo'] = 1
            elif _deal_result[0] == 'error':
                itchat.send(_deal_result[1], toUserName=_from_username)
            elif _deal_result[0] == 'success':
                itchat.send(_deal_result[1], toUserName=_from_username)
            elif _deal_result[0] == 'hurry':
                itchat.send(_deal_result[1])
                itchat.send('后台没有登陆系统，等待管理员操作，完成后将自动回复指令，请稍等~', toUserName=_from_username)

            # 判断循环是否终止
            if self.config_list.get('iot_todo') == 1:
                _response = self.deal_todo_order('iot', _from_username)
                # 返回一个list:['operate_ok', _from_username, _order_name, order_param] 或者none

                if _response is None:
                    self.config_list['iot_todo'] = 0
                    break
            else:
                break
        #
        #
        #
        # else:
        #     _at = ''
        #     if _from_username[0:2] == '@@':
        #         # 证明是群聊天
        #
        #         _is_friend = itchat.search_friends(userName=msg.ActualUserName)
        #         # 返回None，或搜索结果
        #
        #         if _is_friend is None:
        #             _at = '@' + msg['ActualNickName'] + '\n'
        #         else:
        #             _at = '@' + _is_friend.NickName + '\n'
        #

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
                if b == 'iot':
                    process.import_reload('iot_system')
                    print('iot_system reload is done')
                elif b == 'process':
                    imp.reload(process)
                    print('process reload is done')
                elif b == 'system':
                    process.import_reload('cn_system')
                    print('cn_system reload is done')
                else:
                    itchat.send(a)
            # 这里要继续补充


thread1 = MyThread(1, 'thread-1', 1)
thread1.start()

r = requests.session()
cn_order_list = {}
cn_chart_list = {}
# cn_order_list表示待办理的命令
# cn_chart_list表示待回复的对话

cn_config_list={}
# 同步一些配置和开关

cn_msg_process = CnMsgProcess(cn_order_list, cn_chart_list, cn_config_list,r)
# def __init__(self, msg, cn_order_list, cn_chart_list)

main(cn_msg_process)
