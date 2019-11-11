import itchat
from itchat.content import TEXT,PICTURE, RECORDING, ATTACHMENT, VIDEO
import threading
from process import CnMsgProcess,CnMsgProcess_kivy
import platform
import requests
import process
import importlib as imp
import time


def to_front_desk_text(kivy, msg):
	_from_username = msg.FromUserName
	_text = msg.Text
	_member_list_name = msg.User.RemarkName
	if _member_list_name == '':
		_member_list_name = msg.User.NickName
	if _from_username[0:2] == '@@':
		_group_chat_name = msg.ActualNickName
	else:
		_group_chat_name = ''

	kivy.add_member_list(_from_username, _member_list_name)
	kivy.msg_receive(_from_username, _text, _group_chat_name)

def to_front_desk_img(kivy, msg, _img_path):
	_from_username = msg.FromUserName
	_member_list_name = msg.User.NickName
	_text = msg.Text

	if _from_username[0:2] == '@@':
		_group_chat_name = msg.ActualNickName
	else:
		_group_chat_name = ''

	kivy.add_member_list(_from_username, _member_list_name)
	kivy.img_receive(_from_username, _img_path, _group_chat_name)

#         _is_friend = itchat.search_friends(userName=msg.ActualUserName)
        # if(msg.FromUserName!='@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d'):
        
def to_back_desk(msg_process, msg):
	_from_username = msg.FromUserName
	_response = msg_process.cn_msg_process(msg)
	# 返回结果是一个 list
	# ['operate_ok', _from_username, _order_name, order_param]
	
	while True:
	# while：目的是当系统登陆前一些待办命令需要在系统登陆后马上处理
	
		_deal_result = msg_process.cmcc_process(_response)
		to_weixin(_deal_result, _from_username, msg_process)
		
		# 判断循环是否终止
		if msg_process.config_list.get('iot_todo') == 1:
			_response = msg_process.deal_todo_order('iot', _from_username)
			# 返回一个list:['operate_ok', _from_username, _order_name, order_param] 或者none
		
			if _response is None:
				msg_process.config_list['iot_todo'] = 0
				break
		else:
			break

def to_weixin(_deal_result, _from_username, msg_process):
	if _deal_result is None:
		return
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
			msg_process.config_list['iot_todo'] = 1
	elif _deal_result[0] == 'error':
		itchat.send(_deal_result[1], toUserName=_from_username)
	elif _deal_result[0] == 'success':
		itchat.send(_deal_result[1], toUserName=_from_username)
	elif _deal_result[0] == 'hurry':
		itchat.send(_deal_result[1])
		itchat.send('后台没有登陆系统，等待管理员操作，完成后将自动回复指令，请稍等~', toUserName=_from_username)


def itchat_main(msg_process, kivy_process):
	@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True)
	def chat_receive(msg):
		to_front_desk_text(kivy_process, msg)
		to_back_desk(msg_process, msg)


	@itchat.msg_register(PICTURE)
	def download_files(msg):
		# _file_dir = 'client/'+msg.User.NickName+'/img/'+msg.fileName
		print(msg.fileName)
		_file_dir = 'client/' + msg.fileName
		msg.download(_file_dir)
		kivy_process.show_img('receive', _file_dir)
		# itchat.send('@%s@%s' % ('img' if msg['Type'] == 'Picture' else 'fil', msg['FileName']),msg['FromUserName'])
		# return '%s received' % msg['Type']
	

	itchat.auto_login(hotReload=True)
	itchat.run()


def start(_kivy):
	thread_kivy = kivy_start_itchat_thread(_kivy)
	thread_kivy.start()


class kivy_start_itchat_thread(threading.Thread):
	def __init__(self, _kivy):
		threading.Thread.__init__(self)
		self.kivy = _kivy

	def run(self):
		order_list = {}
		chat_list = {}
		# order_list表示待办理的命令
		# chat_list表示待回复的对话
		
		config_list = {}
		# 同步一些配置和开关

		r = requests.session()
		
		msg_process = process.CnMsgProcess()
		itchat_main(msg_process, self.kivy)
		# itchat_main(self.kivy)


