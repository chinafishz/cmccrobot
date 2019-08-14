import itchat
from itchat.content import TEXT
import threading
from process import CnMsgProcess


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
                itchat.send(b[1],b[0])
            elif len(b) == 1:
                itchat.send(a)


def main(self):
    @itchat.msg_register(TEXT,isFriendChat=True)
    # isGroupChat=True
    def simple_reply(msg):
        _from_username = msg.FromUserName
        _to_username = msg.ToUserName
        _text = msg.Text
        _response = self.cn_msg_process(msg)
        if _response is not None:
            itchat.send('@'+msg.User.NickName+' '+_response)
        #a.setdefault('chinafishz',{'ordername':'#puk','param':{}}).setdefault('param',{'c':3,'b':2}).update({'c':3,'b':2})
        # if(msg.FromUserName!='@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d'):
        #     print('【接收】'+msg.User.RemarkName+':'+msg.Text,msg.FromUserName)
        # elif(msg.FromUserName=='@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d'):
        #     if(msg.ToUserName=='@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d'):
        #         print('【自己】' + msg.Text, msg.FromUserName)
        #     else:
        #         print('【发给】'+msg.User.RemarkName+':'+msg.Text,msg.ToUserName)

    # itchat.auto_login(hotReload=True)
    itchat.auto_login(hotReload=True,enableCmdQR=2)

    itchat.run()


thread1 = MyThread(1,'thread-1',1)
thread1.start()


cn_order_list = {}
cn_chart_list = {}
# cn_order_list表示待办理的命令
# cn_chart_list表示待回复的对话

cn_process = CnMsgProcess(cn_order_list,cn_chart_list)
# def __init__(self, msg, cn_order_list, cn_chart_list)

main(cn_process)


