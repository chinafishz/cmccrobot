import itchat
from itchat.content import TEXT
import threading
#from process import CnMsgProcess

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




def mai(cn_process):
    @itchat.msg_register(TEXT,isFriendChat=True) #isGroupChat=True
    def simple_reply(msg):
        _from_username = msg.FromUserName
        _tousername = msg.ToUserName
        _text = msg.Text
        _reponse=cn_process.cn_msg_process(msg)
        
        itchat.send('返回结果:'+_from_username)
        #
        # if(msg.FromUserName!='@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d'):
        #     print('【接收】'+msg.User.RemarkName+':'+msg.Text,msg.FromUserName)
        # elif(msg.FromUserName=='@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d'):
        #     if(msg.ToUserName=='@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d'):
        #         print('【自己】' + msg.Text, msg.FromUserName)
        #     else:
        #         print('【发给】'+msg.User.RemarkName+':'+msg.Text,msg.ToUserName)

    #itchat.auto_login(hotReload=True)
    
    itchat.auto_login(hotReload=True,enableCmdQR=2)
    itchat.run()




thread1=mythread(1,'thread-1',1)
thread1.start()


cn_order_list={}
cn_chart_list={}
#cn_order_list表示待办理的命令
#cn_chart_list表示待回复的对话

cn_process=CnMsgProcess(cn_order_list,cn_chart_list)
main(cn_process)

