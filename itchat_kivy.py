import itchat
from itchat.content import TEXT, PICTURE, RECORDING, ATTACHMENT, VIDEO
import threading
from process import CnMsgProcess, CnMsgProcess_kivy
import platform
import requests
import process
import importlib as imp
import time
import os
# from PIL import Image
import math


def group_icon_join(_group_name):
	group_icon_path = os.path.join('group', _group_name, 'icon')
	files = os.listdir(group_icon_path)
	each_size = int(math.sqrt(float(750 * 750) / len(files)))
	lines = int(750 / each_size)
	image = Image.new('RGB', (750, 750))
	x = 0
	y = 0
	for _icon in files:
		img = Image.open(os.path.join(group_icon_path, _icon))
		img = img.resize((each_size, each_size), Image.ANTIALIAS)
		image.paste(img, (x * each_size, y * each_size))
		x = x + 1
		if x == lines:
			x = 0
			y = y + 1
	image.save(os.path.join(group_icon_path,'main.jpg'))


def to_front_desk_text(kivy, msg):
	_from_username = msg.User.UserName
	_member_list_name = ''
	_text = msg.Text

	# if from  username is me
	if _from_username != '@146bc331344a6eedc213bed5b29fa465e26a6673b52b566f74e45fb2adf6dd9d':
		try:
			# 发现会出现不存在remarkname参数
			_member_list_name = msg.User.RemarkName
		except:
			_member_list_name = ''

		if _member_list_name == '':
			try:
				_member_list_name = msg.User.NickName
			except:
				print(msg.User)
	else:
		_from_username = msg.ToUserName

	if _from_username[0:2] == '@@':
		try:
			_group_user_name = msg.User.RemarkName
		except:
			_group_user_name == ''
		if _group_user_name == '':
			_group_user_name = msg.ActualNickName
	else:
		_group_user_name = ''


	a = kivy.add_member_list(_from_username, _member_list_name)


	kivy.msg_receive(_from_username, _text, _group_user_name)


'''
群：
群名称：msg.User.NickName
群成员有备注：msg.ActualNickName


个人：
有备注：msg.User.RemarkName
没有备注：msg.User.NickName

'''
def to_front_desk_img(kivy, msg, _img_path):
	_from_username = msg.User.UserName

	if _from_username[0:2] == '@@':
		_member_list_name = msg.User.NickName
	else:
		_member_list_name = msg.User.RemarkName
		if _member_list_name == '':
			_member_list_name = msg.User.NickName

	kivy.add_member_list(_from_username, _member_list_name)

	try:
		kivy.show_img('receive', _img_path, _from_username)
	except:
		print('错误4401')


def to_front_desk_file(kivy, msg, _file_path):
	_from_username = msg.User.UserName
	_member_list_name = msg.User.RemarkName
	if _member_list_name == '':
		_member_list_name = msg.User.NickName

	if _from_username[0:2] == '@@':
		_group_chat_name = msg.ActualNickName
	else:
		_group_chat_name = ''

	kivy.add_member_list(_from_username, _member_list_name, kivy)
	
	_file_temp = _file_path.split('/')
	_file_name = _file_temp[len(_file_temp) - 1]
		
	kivy.show_file('receive', _file_path, _file_name, _from_username)


def to_back_desk(msg_process, msg):
	_from_username = msg.User.UserName
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

def to_weixin(_deal_result, _from_username, msg_process=None):
	if _deal_result is None:
		return
	elif _deal_result[0] == '4a_login_up':
		itchat.send('需要登陆4A，请回复验证码')
		itchat.send(_deal_result[1])
		itchat.send('后台没有登陆系统，等待管理员操作，完成后将自动回复指令，请稍等~', toUserName=_from_username)
	elif _deal_result[0] == '4a_login_up_success':
		itchat.send('成功登陆4A')
		for _i in _deal_result[1].split(';'):
			if _i.split('|')[0] in ['广东移动NGESOP系统', '广州NGBOSS前台', '物联网系统前台']:
				itchat.send(_i)
	elif _deal_result[0] == 'iot_login_up':
		itchat.send('成功登陆iot系统')
		msg_process.config_list['iot_todo'] = 1
	elif _deal_result[0] == 'Warning':
		itchat.send(_deal_result[1], toUserName=_from_username)
		itchat.send(_deal_result[2])
	elif _deal_result[0] == 'error':
		itchat.send(_deal_result[1], toUserName=_from_username)
	elif _deal_result[0] == 'success':
		itchat.send(_deal_result[1], toUserName=_from_username)
	elif _deal_result[0] == 'hurry':
		itchat.send(_deal_result[1])
		itchat.send('后台没有登陆系统，等待管理员操作，完成后将自动回复指令，请稍等~', toUserName=_from_username)


'''
群：
群名称：msg.User.NickName
群成员有备注：msg.ActualNickName


个人：
有备注：msg.User.RemarkName
没有备注：msg.User.NickName

'''
def to_laopo(_type, msg, kivy, _path=None):
	if msg.User.UserName[0:2] != '@@':
		return
	try:
		_group_name = msg.User.NickName
	except:
		_group_name = ""

	if _group_name in ['测试群']:
		_user_name = msg.ActualNickName

		if _type == TEXT:
			itchat.send('[' + _group_name + ']' + _user_name + ':\n' + msg.text, toUserName=kivy.laopo_username)
		elif _type == PICTURE:
			itchat.send('[' + _group_name + ']' + _user_name + ':', toUserName=kivy.laopo_username)
			itchat.send_image(_path, toUserName=kivy.laopo_username)
		elif _type in [ATTACHMENT, RECORDING]:
			itchat.send('[' + _group_name + ']' + _user_name + ':', toUserName=kivy.laopo_username)
			itchat.send_file(_path, toUserName=kivy.laopo_username)
		elif _type in [VIDEO]:
			itchat.send('[' + _group_name + ']' + _user_name + ':', toUserName=kivy.laopo_username)
			itchat.send_video(_path, toUserName=kivy.laopo_username)

	pass


def check_file_path(_file_path):
	# 改位置如果有新增的文件夹，需要补充，每个用户首次出现，都建立所有附件文件夹
	if os.path.exists(os.path.join(_file_path, 'files')) is False:
		os.makedirs(os.path.join(_file_path, 'files'))

	if os.path.exists(os.path.join(_file_path, 'img')) is False:
		os.makedirs(os.path.join(_file_path, 'img'))

	if os.path.exists(os.path.join(_file_path, 'icon')) is False:
		os.makedirs(os.path.join(_file_path, 'icon'))

def itchat_main(msg_process, kivy_process):
	@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True)
	def chat_receive(msg):
		to_front_desk_text(kivy_process, msg)
		to_back_desk(msg_process, msg)
		to_laopo(msg.type, msg, kivy_process)

	'''
	群：
	群名称：msg.User.NickName
	群成员有备注：msg.ActualNickName


	个人：
	有备注：msg.User.RemarkName
	没有备注：msg.User.NickName

	'''
	@itchat.msg_register([PICTURE, ATTACHMENT, VIDEO], isFriendChat=True, isGroupChat=True)
	def download_media(msg):
		_from_username = msg.User.UserName


		if _from_username[0:2] == '@@':
			_name = msg.User.NickName
			_file_dir = os.path.join('group', _name)
		else:
			_name = msg.User.RemarkName
			if _name == '':
				_name = msg.User.NickName
			_file_dir = os.path.join('client',_name)

		check_file_path(_file_dir)
		
		if msg.type == PICTURE:
			_file_path = os.path.join(_file_dir,'img', msg.fileName)
			msg.download(_file_path)
			to_front_desk_img(kivy_process, msg, _file_path)

		else:
			_file_path = os.path.join(_file_dir, 'files', msg.fileName)
			msg.download(_file_path)
			to_front_desk_file(kivy_process, msg, _file_path)

		to_laopo(msg.type, msg, kivy_process, _file_path)

	@itchat.msg_register([RECORDING], isFriendChat=True, isGroupChat=True)
	def download_media(msg):
		_from_username = msg.ToUserName

		if _from_username[0:2] == '@@':
			__name = msg.ActualUserName

			_file_dir = os.path.join('group', 'temp')
		else:
			_name = msg.User.RemarkName
			if _name == '':
				_name = msg.User.NickName
			_file_dir = os.path.join('client', _name)

		check_file_path(_file_dir)

		_file_path = os.path.join(_file_dir, 'files', msg.fileName)
		msg.download(_file_path)

		to_laopo(msg.type, msg, kivy_process, _file_path)

	itchat.auto_login(hotReload=True)

	# 将好友列表、群组导入内存,采用覆盖写入
	kivy_process.get_contact()

	# 获取好友头像
	kivy_process.get_client_icon()

	# 运行itchat后读取老婆的username
	kivy_process.laopo_username = kivy_process.search_contact_setp1('老婆专用群')[1]['老婆专用群']['username']

	itchat.run()
	

def start(_kivy):
	thread_kivy = kivy_start_itchat_thread(_kivy)
	thread_kivy.start()


class kivy_start_itchat_thread(threading.Thread):
	def __init__(self, _kivy):
		threading.Thread.__init__(self)
		self.kivy = _kivy

	def run(self):
		msg_process = process.CnMsgProcess()	
		itchat_main(msg_process, self.kivy)
