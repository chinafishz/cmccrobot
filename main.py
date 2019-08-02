import itchat
from itchat.content import TEXT
import threading
from process import CnMsgProcess

class mythread(threading.Thread):
    def __init__(self,threadID,name,counter):
        threading.Thread.__init__(self)
        self.threadID=threadID
        self.name=name
        self.counter=counter

    def run(self):
        while(True):
            a=input()
            # print(a)
            b=a.split(' ')
            # print(b)
            if(len(b)==2):
                itchat.send(b[1],b[0])
            elif(len(b)==1):
                itchat.send(a)



def main():
    @itchat.msg_register(TEXT,isFriendChat=True) #isGroupChat=True,
    def simple_reply(msg):
        cn_from_username = msg.FromUserName
        cn_tousername = msg.ToUserName
        cn_text = msg.Text
        cn_order_list={} # 字典格式为 {@fromuser:{ordername,plan_type,param_supple}
        cn_reponse=CnMsgProcess.cn_msg_process(msg,cn_from_username,cn_order_list)
        itchat.send('返回结果:'+cn_reponse,cn_from_username)
        #
        # if(msg.FromUserName!='@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d'):
        #     print('【接收】'+msg.User.RemarkName+':'+msg.Text,msg.FromUserName)
        # elif(msg.FromUserName=='@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d'):
        #     if(msg.ToUserName=='@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d'):
        #         print('【自己】' + msg.Text, msg.FromUserName)
        #     else:
        #         print('【发给】'+msg.User.RemarkName+':'+msg.Text,msg.ToUserName)

    itchat.auto_login(hotReload=True)
    itchat.run()




thread1=mythread(1,'thread-1',1)
thread1.start()

main()

