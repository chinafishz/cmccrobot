from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')

Config.set('kivy', 'default_font', ['msgothic','font/DroidSansFallback.ttf'])

import sys
sys.setrecursionlimit(1000000)

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.checkbox import CheckBox
import warnings
import string
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import DictProperty
from kivy.properties import ListProperty
import itchat
import itchat_kivy
import time
from kivy.config import Config
import kivy
import random
from kivy.clock import Clock
from functools import partial
from kivy.core.window import Window
import os
from kivy.storage.jsonstore import JsonStore
from kivy.uix.behaviors import FocusBehavior
import json
import configparser
from kivy.uix.image import AsyncImage

# 初始化字体，放在font目录下
kivy.resources.resource_add_path("font/")
cn_font_1 = kivy.resources.resource_find("DroidSansFallback.ttf")


class MemberList_ToggleButton(ToggleButton):
	size_hint = [1, None]
	img_path = StringProperty('')
	_id = StringProperty('')
	btn_height = NumericProperty(65)
	btn_texture_size = ListProperty([200,25])





class ScrollClass(ScrollView):
	pass


class BackgroundColor(Widget):
	pass


class LeftWidget(Widget):
	pass

class MiddleWidget(Widget):
	pass

class RightWidget(Widget):
	pass

class ChatWindow(BoxLayout):
	orientation = 'vertical'


class ChatLabel(Label):
	markup = True
	valign = 'centre'

class FileChoosDialog(BoxLayout):
	load = ObjectProperty(None)
	window = ObjectProperty(None)

class KivyWindow(Widget):
	def test(self):
		a = u'client/'+ '贤贤娃' +u'/icon/main.jpg'

		self.ids.member_list.children[0].img_path = a

	def test1(self):
		b=self.ids.member_list.children[0].children[1]
		b.reload()

	# kivy配置文件
	kivy_config = configparser.ConfigParser()

	# 将全局字体引入到这个widget，供kv文件调用
	cn_font_1 = cn_font_1

	# 对话记录
	chat_record = {}

	# 目前member的数量，动态变化
	member_item_count = NumericProperty(0)

	# 设置chat_window的高度
	chat_window_height = NumericProperty(0)

	# member_list当前选择的是那个item, type is togglebutton
	member_list_current = ObjectProperty(None)

	# 窗口是否关闭，true则不关
	window_keep_open = True

	# 图片下载待办列表
	img_download_task = []

	# 记录键盘长按按钮
	keyboard_down_array = []

	# 记录静音明细
	mute_array = []

	# 窗口分布
	kivy_config_layout = DictProperty({'LayoutSize':{'left_size':260, 'right_size':260}})

	# 获取老婆的username
	laopo_username = ''

	# 设置左栏member的高度
	member_item_height = NumericProperty(65)

	image_queue={}

	def __init__(self, **kwargs):
		super(KivyWindow, self).__init__(**kwargs)
		self.ids.chat_scroll.add_widget(StackLayout(orientation='tb-lr', size_hint=[1, None]))
		Window.bind(on_request_close=self.exit_check)
		# self.member_list_current = self.ids.togglebutton_filehelper

		# 绑定静音chekbox
		self.ids.title_checkbox_is_mute.bind(active = self.title_checkbox_is_mute_active)


		self.kivy_config.read("KivyConfig.ini")

		# 读取静音数据
		# 返回mute_array的是list格式，写入ini文件是str格式，要做转换
		self.mute_array = self.kivy_config.get('Lists', 'chat_mute_array').split(',')

		# 读取布局数据
		self.kivy_config_layout.update({'LayoutSize':{'left_size':int(self.kivy_config.get('LayoutSize','left_size')), 'right_size':int(self.kivy_config.get('LayoutSize','right_size'))}})




		pass


	# ——————————————————————————————————以下为左侧部分——————————————————————————————————
	# 搜索通讯录
	# 目前只做了搜索好友，其他没有
	def search_contact(self):
		_step1 = self.search_contact_setp1()
		if _step1 is not False:
			self.search_contact_setp2(_step1[0], _step1[1])

	def search_contact_setp1(self, _input=None):
		if self.ids.contact_textinput_name.text == '' and _input is None:
			return False

		if _input is None:
			_search_input = ''.join(self.ids.contact_textinput_name.text.lower()).split()
		else:
			_search_input = _input.split()

		if _search_input.__len__() == 0 and _input is None:
			return

		# 目前暂时不能多关键字搜索，先设定默认取第一个关键字
		_search_input = _search_input[0]
		self.ids.contact_textinput_name.text = ''

		# 搜索结果
		with open('ContactList.json', 'r') as result_file:
			_contact_list = json.load(result_file)


		# 格式为： {name1:username1，name2:username2}
		_result_friend = {}
		_result_room = {}

		# 历遍通讯录
		for _user_name, _user_dic in _contact_list.items():
			_search_result_name = _user_dic.get('name').find(_search_input)
			_search_result_pinyin = _user_dic.get('namepinyin').find(_search_input)
			_search_result_headimurl = _user_dic.get('headimgurl')
			if _search_result_name != -1 or _search_result_pinyin != -1:
				if _user_dic.get('type') == 'f':
					_result_friend.update({_user_dic.get('name'): {'username':_user_name, 'headimgurl':_search_result_headimurl}})
				elif _user_dic.get('type') == 'r':
					_result_room.update({_user_dic.get('name'): {'username':_user_name, 'headimgurl':_search_result_headimurl}})

		return [_result_friend,_result_room]

	def search_contact_setp2(self,_result_friend, _result_room):
		_main = BoxLayout()
		_popup = Popup(title='搜索结果', title_font=cn_font_1)
		# 显示好友搜索结果
		_scroll_friends = ScrollView(size_hint=[1, 1])
		_box_friends = StackLayout(spacing=[5, 5], size_hint=[1, None])
		for _result_name, _result_value in _result_friend.items():
			_btn = Button(text=_result_name, font_name=cn_font_1, size_hint=[0.25, None])
			_btn._id = _result_value['username']
			_btn.bind(on_release=partial(self.search_result_choose, _popup))
			_box_friends.add_widget(_btn)
		_scroll_friends.add_widget(_box_friends)
		_box_friends.height = self.height / 9 * (int(len(_result_friend) / 4) + 1)
		_scroll_friends.height = self.height * 0.8

		# 显示群组搜索结果
		_scroll_rooms = ScrollView(size_hint=[1, 1])
		_box_rooms = StackLayout(spacing=[5, 5], size_hint=[1, None])
		for _result_name, _result_value in _result_room.items():
			_btn = Button(text=_result_name, font_name=cn_font_1, size_hint=[0.25, None])
			_btn._id = _result_value['username']
			_btn.bind(on_release=partial(self.search_result_choose, _popup))
			_box_rooms.add_widget(_btn)
		_scroll_rooms.add_widget(_box_rooms)
		_box_rooms.height = self.height / 9 * (int(len(_result_room) / 4) + 1)
		_scroll_rooms.height = self.height * 0.8

		_main.add_widget(_scroll_friends)
		_main.add_widget(_scroll_rooms)
		_popup.content = _main
		_popup.open()

	def search_result_choose(self, _popup, _btn, *args):
		_popup.dismiss()
		_name = _btn.text
		_id = _btn._id


		_togglebutton = self.add_member_list(_id, _name)
		_togglebutton.background_color = [0,0,0,0]
		_togglebutton.state = 'down'
		self.member_list_current.state = 'normal'
		try:
			self.member_list_change(_togglebutton)
		except:
			print('错误4405', type(_togglebutton))

	# 如果_update=True，则重新更新好友列表
	# 该程序在itchat_kivy.py文件初始化时运行
	def get_contact(self, _update=False):
		# _friends_list 为多个用户的所有字段结果
		_friends_list = itchat.get_friends(_update)
		_room_list = itchat.get_chatrooms(_update)
		_result = {}

		for _user in _friends_list:
			if _user.RemarkName != '':
				_name = _user.RemarkName
				try:
					_pinyin = _user.RemarkPYQuanPin
				except:
					_pinyin = '【ERROR：没有数据】'
			else:
				_name = _user.NickName
				_pinyin = _user.PYQuanPin
			_result.update({_user.UserName:{'type':'f', 'name':_name, 'namepinyin':_pinyin}})

		for _room in _room_list:
			if _room.RemarkName != '':
				_name = _room.RemarkName
			else:
				_name = _room.NickName

			try:
				_pinyin = _room.PYQuanPin
			except:
				_pinyin = '【ERROR：没有数据】'

			_result.update({_room.UserName:{'type':'r', 'name':_name, 'namepinyin':_pinyin}})

		with open('ContactList.json', 'w') as result_file:
			json.dump(_result, result_file)

		print('已经获取通讯录')

	def callback_get_contact(self, *args):
		pass


	'''
	群：
	群名称：msg.User.NickName
	群成员有备注：msg.ActualNickName

	个人：
	有备注：msg.User.RemarkName
	没有备注：msg.User.NickName
	'''
	# 获取头像
	def get_client_icon(self):

		with open('ContactList.json', 'r') as result_file:
			_contact_list = json.load(result_file)

		_a = 0
		for i in _contact_list.items():
			_username = i[0]
			if _username[0:2] == '@@':
				continue

			_value = i[1]['name']
			_value = _value.replace('/','')
			_client_icon_file = os.path.join('client', _value, 'icon', 'main.jpg')

			if os.path.exists(_client_icon_file) is False:
				_client_dir = os.path.join('client', _value)
				_client_file_dir = os.path.join(_client_dir, 'icon')

				if os.path.exists(_client_dir) is False:
					os.mkdir(_client_dir)

				if os.path.exists(_client_file_dir) is False:
					os.mkdir(_client_file_dir)


				# 获取头像
				try:
					img_data = itchat.get_head_img(userName=_username)
					with open(_client_icon_file, 'wb') as file:
						file.write(img_data)
				except:
					print(_a, _value)

			_a = _a+1
		print("已经获取全部个人头像")


	def add_member_list(self, _id, _name, _kivy=None, _msg=None):
		if _kivy is None:
			_kivy =self
		if _id in self.chat_record.keys():
			# 已经存在的聊天，只需要修改顺序和颜色
			# 新消息提醒，按钮底色变红
			for i in self.ids.member_list.children:
				# i 是boxlayout
				if i.children[0]._id == _id:
					# 将新消息放在最前 ,children[0]为一个，没考虑永久置顶的因素
					self.ids.member_list.remove_widget(i)
					self.ids.member_list.add_widget(i)

					# 将新消息底色标黄
					if _name not in self.mute_array:
						i.children[0].background_color = [2, 2, 0, 1]
					return i
		else:
			# 不存在的聊天，需要新增
			self.member_item_count = self.member_item_count + 1
			if _id[0:2] == '@@':
				_icon_path = os.path.join('group', _name, 'icon', 'main.jpg')
			else:
				_icon_path = os.path.join('client', _name, 'icon', 'main.jpg')

			_hint = (self.member_item_height - 10) / self.kivy_config_layout['LayoutSize']['left_size']
			MemberList_ToggleButton_Image = AsyncImage(source=_icon_path, nocache=True, size_hint_x= _hint , size_hint_y=None, size=[self.member_item_height,self.member_item_height])


			MemberList_ToggleButton =ToggleButton(text=_name, height=self.member_item_height, group='cmcc', size_hint_x=1-_hint, size_hint_y=None, valign='top')
			MemberList_ToggleButton.texture_update()
			MemberList_ToggleButton.text_size = [self.kivy_config_layout['LayoutSize']['left_size']-self.member_item_height-10 , self.member_item_height-10]
			MemberList_ToggleButton._id = _id
			MemberList_ToggleButton.bind(on_release=self.member_list_change)
			if _name not in self.mute_array:
				MemberList_ToggleButton.background_color = [2, 2, 0, 1]

			_box = BoxLayout(size_hint_x= 1, size_hint_y=None, height=self.member_item_height, padding=[0,5,0,5])




			_box.add_widget(MemberList_ToggleButton_Image)
			_box.add_widget(MemberList_ToggleButton)
			self.ids.member_list.add_widget(_box)



			self.chat_record.update({_id:None})
			
			if self.member_list_current is None:
				self.member_list_current = MemberList_ToggleButton
				
			return MemberList_ToggleButton

	def member_list_change(self, _togglebutton):
		if _togglebutton._id == self.member_list_current._id:
			_togglebutton.background_color = [1,1,1,1]
			_togglebutton.state = 'down'
			return
		else:
			_togglebutton.background_color = [1,1,1,1]
			self.member_list_current.background_color = [0,0,0,0]
			self.record_chat()
			self.member_list_current = _togglebutton
			self.read_chat_record()

		self.ids.chat_title.text = _togglebutton.text
		self.ids.chat_scroll.scroll_y = 0

		if self.member_list_current.text in self.mute_array:
			self.ids.title_checkbox_is_mute.active = True
		else:
			self.ids.title_checkbox_is_mute.active = False


	# ——————————————————————————————————以下为中部部分——————————————————————————————————

	# 静音设置
	def title_checkbox_is_mute_active(self, *args):
		if args[1]is True and self.member_list_current.text not in self.mute_array:
			self.mute_array.append(self.member_list_current.text)
		elif args[1]is False and self.member_list_current.text in self.mute_array:
			self.mute_array.remove(self.member_list_current.text)

		# 保存到配置文件
		self.kivy_config.set('Lists', 'chat_mute_array', ','.join(self.mute_array))
		with open('KivyConfig.ini', 'w')as conf:
			self.kivy_config.write(conf)

	# 发送健效果
	def msg_send(self):
		_text = self.ids.weixin_textinput.text
		if _text == '':
			return
		itchat.send(_text, toUserName=self.member_list_current._id)
		self.show_label('send', _text, self.member_list_current._id)
		self.ids.weixin_textinput.text = ''

	def msg_receive(self, _id, _text, _name=''):
		if _name != '':
			_name = _name + ': '
		self.show_label('receive', _name + _text, _id)

	def record_chat(self):
		self.chat_record.update({self.member_list_current._id: self.ids.chat_scroll.children[0]})

	def read_chat_record(self):
		# this time member_list_current is chang to new usename
		_new_chat_record = self.chat_record.setdefault(self.member_list_current._id, None)
		_now_chat_widget = self.ids.chat_scroll.children[0]
		self.ids.chat_scroll.remove_widget(_now_chat_widget)

		if _new_chat_record is None:
			self.chat_window_height = 30
			self.ids.chat_scroll.add_widget(StackLayout(orientation='tb-lr', size_hint=[1, None]))
		else:
			self.chat_window_height = _new_chat_record.height
			self.ids.chat_scroll.add_widget(_new_chat_record)

	# 展示图片
	def show_img(self, _type, _img_path, _chat_window_id):
		_chat_window = None
		_chat_scroll = self.ids.chat_scroll

		if _chat_window_id == self.member_list_current._id:
			_chat_window = _chat_scroll.children[0]
		else:
			_chat_window = self.chat_record.setdefault(_chat_window_id, None)
			if _chat_window is None:
				_chat_window = StackLayout(orientation='tb-lr', size_hint=[1, None])
				_chat_window.width = _chat_scroll.width
				_chat_window.height = 0

		_label_left = Label()

		_label_main = AsyncImage(source=_img_path, nocache=True)
		# _label_main.reload()
		_label_main.bind(on_touch_down=self.zoom_img)
		_label_main.size = [_label_main.norm_image_size[0], _label_main.norm_image_size[1]]
		_label_right = Label()

		_pos_x_hint_left = [0, 0]
		_pos_x_hint_main = [0, 0]
		_pos_x_hint_right = [0, 0]

		while _pos_x_hint_main[0] == 0:
			if _label_main.texture_size[0] >= _chat_window.width * 0.7:

				_pos_x_hint_main = [0.7, None]
			else:
				_pos_x_hint_main = [_label_main.texture_size[0] / _chat_window.width, None]

		if _type == 'receive':
			_pos_x_hint_left = [0.05, None]
			_pos_x_hint_right = [1 - _pos_x_hint_left[0] - _pos_x_hint_main[0], None]
		elif _type == 'send':
			_pos_x_hint_left = [1 - 0.05 - _pos_x_hint_main[0], None]
			_pos_x_hint_right = [0.05, None]
		elif _type == 'time':
			_pos_x_hint_left = [(1 - _pos_x_hint_main[0]) / 2, None]
			_pos_x_hint_right = _pos_x_hint_left

			_chat_window.last_msg_time = time.time()

		_label_left.size_hint = _pos_x_hint_left
		_label_main.size_hint = _pos_x_hint_main
		_label_right.size_hint = _pos_x_hint_right

		_box = BoxLayout(size_hint=[1, None])
		_box.height = _label_main.texture_size[1] + 30
		_box.add_widget(_label_left)
		_box.add_widget(_label_main)
		_box.add_widget(_label_right)
		_chat_window.add_widget(_box)

		if _chat_window_id is None:
			# _chat_scroll.scroll_y = 0
			self.chat_window_height = self.chat_window_height + _box.height
			_chat_window.height = self.chat_window_height + 30
		else:
			_chat_window.height = _chat_window.height + _box.height
			self.chat_record.update({_chat_window_id: _chat_window})

		pass

	# 展示label到scroll
	def show_label(self, _type, _text, _chat_window_id=None):
		# show_label can record to all chat,not only current chat
		_chat_window = None
		_chat_scroll = self.ids.chat_scroll

		if _chat_window_id == self.member_list_current._id:
			_chat_window = _chat_scroll.children[0]
		else:
			_chat_window = self.chat_record.setdefault(_chat_window_id, None)
			if _chat_window is None:
				_chat_window = StackLayout(orientation='tb-lr', size_hint=[1, None])
				_chat_window.width = _chat_scroll.width
				_chat_window.height = 0
		_label_left = Label()
		_label_main = ChatLabel(text=_text, font_name=cn_font_1)
		_label_right = Label()

		_pos_x_hint_left = [0, 0]
		_pos_x_hint_main = [0, 0]
		_pos_x_hint_right = [0, 0]

		while _pos_x_hint_main[0] == 0:
			if _type != 'send':
				time.sleep(1)
			else:
				_label_main.texture_update()
			#  通过kivy自身操作是texture_size不会自动更新,但外部调用也会更新，所以send操 /
			#  作时增加texture_update

			if _label_main.texture_size[0] >= _chat_window.width * 0.7:
				_label_main.text_size = [_chat_window.width * 0.7, None]
				_pos_x_hint_main = [0.7, None]
			else:
				_pos_x_hint_main = [_label_main.texture_size[0] / _chat_window.width, None]

		if _type == 'receive':
			_pos_x_hint_left = [0.05, None]
			_pos_x_hint_right = [1 - _pos_x_hint_left[0] - _pos_x_hint_main[0], None]
		elif _type == 'send':
			_pos_x_hint_left = [1 - 0.05 - _pos_x_hint_main[0], None]
			_pos_x_hint_right = [0.05, None]

		_label_left.size_hint = _pos_x_hint_left
		_label_main.size_hint = _pos_x_hint_main
		_label_right.size_hint = _pos_x_hint_right

		_box = BoxLayout(size_hint=[1, None])
		_box.height = _label_main.texture_size[1] + 50
		_box.add_widget(_label_left)
		_box.add_widget(_label_main)
		_box.add_widget(_label_right)
		_chat_window.add_widget(_box)

		if _chat_window_id is None:
			# _chat_scroll.scroll_y = 0
			self.chat_window_height = self.chat_window_height + _box.height
			_chat_window.height = self.chat_window_height
		else:
			_chat_window.height = _chat_window.height + _box.height
			self.chat_record.update({_chat_window_id: _chat_window})
		pass

	def show_file(self, _type, _file_path, _file_name, _chat_window_id):
		_chat_window = None
		_chat_scroll = self.ids.chat_scroll

		if _chat_window_id == self.member_list_current._id:
			_chat_window = _chat_scroll.children[0]
		else:
			_chat_window = self.chat_record.setdefault(_chat_window_id, None)
			if _chat_window is None:
				_chat_window = StackLayout(orientation='tb-lr', size_hint=[1, None])
				_chat_window.width = _chat_scroll.width
				_chat_window.height = 0
		_label_left = Label()

		_button_main = Button(text=_file_name)
		_button_main.filepath = _file_path
		# _label_main.bind(on_touch_down=self.zoom_img)
		_label_right = Label()
		_pos_x_hint_main = [0.7, None]

		if _type == 'receive':
			_pos_x_hint_left = [0.05, None]
			_pos_x_hint_right = [0.25, None]
		elif _type == 'send':
			_pos_x_hint_left = [0.25, None]
			_pos_x_hint_right = [0.05, None]

		_label_left.size_hint = _pos_x_hint_left
		_button_main.size_hint = _pos_x_hint_main
		_label_right.size_hint = _pos_x_hint_right

		_box = BoxLayout(size_hint=[1, None])
		_box.height = _button_main.height + 30
		_box.add_widget(_label_left)
		_box.add_widget(_button_main)
		_box.add_widget(_label_right)
		_chat_window.add_widget(_box)

		if _chat_window_id is None:
			# _chat_scroll.scroll_y = 0
			self.chat_window_height = self.chat_window_height + _box.height
			_chat_window.height = self.chat_window_height + 30
		else:
			_chat_window.height = _chat_window.height + _box.height
			self.chat_record.update({_chat_window_id: _chat_window})
		pass

	# def img_receive(self, _img_download_task, *args):
	# 	if len(_img_download_task) > 0:
	# 		# _list为{from_name:图片链接} {keys:values}
	# 		_list = _img_download_task[0]
	#
	# 		self.show_img('receive', list(_list.values())[0], list(_list.keys())[0])
	#
	# 		# 完成后删除
	# 		_img_download_task.remove(_list)

	def send_file(self):
		_content = FileChoosDialog(load=self.filechoose_submit)
		_popup = Popup(title='file choose', content=_content)
		_content.window = _popup
		_popup.open()

	def filechoose_submit(self, _window, _file_path):
		_window.dismiss()
		_file_temp = _file_path.split('.')
		_file_type = _file_temp[len(_file_temp) - 1]
		if _file_type.lower() in ['jpg', 'png', 'jpeg', 'bmp', 'gif']:
			_type = '@img@'
			self.show_img('send', _file_path, self.member_list_current._id)
		else:
			_type = '@fil@'
			_file_temp = _file_path.split('/')
			_file_name = _file_temp[len(_file_temp) - 1]
			self.show_file('send', _file_path, _file_name, self.member_list_current._id)

		itchat.send(_type + _file_path, self.member_list_current._id)

	def zoom_img(self, _widget, touch):
		if _widget.collide_point(*touch.pos):
			_url = _widget.source

			_box = BoxLayout(orientation='vertical')
			_close_btn = Button(text='close', size_hint=[1, 0.08])
			_img = Image(source=_url, size_hint=[1, 0.92])

			_box.add_widget(_img)
			_box.add_widget(_close_btn)

			_popup = Popup(title='Test Pop', content=_box)
			_close_btn.bind(on_release=_popup.dismiss)
			_popup.open()

	# ——————————————————————————————————以下为右侧部分——————————————————————————————————



	# ——————————————————————————————————以下为通用部分——————————————————————————————————
	# 对键盘事件做判定
	def key_process_down(self, _from_target, _key, *args):
		# 微信聊天输入框事件
		if _from_target.target.myid == 'weixin_textinput':
			if _key[0] == 13 and 305 not in self.keyboard_down_array:
				# 回车
				self.msg_send()
			elif _key[0] == 13 and 305 in self.keyboard_down_array:
				# 换行
				_from_target.target.text = _from_target.target.text + '\n'
			else:
				self.key_process_normal(_from_target, _key)
		elif _from_target.target.myid == 'contact_textinput_name':
			if _key[0] == 13 and 305 not in self.keyboard_down_array :
				# 回车
				self.search_contact()
				_from_target.target.focus = False
			else:
				self.key_process_normal(_from_target,_key)
		if _key[0] == 305 and 305 not in self.keyboard_down_array:
			# ctrl
			self.keyboard_down_array.append(305)


	def key_process_up(self, _from_target, _key, *args):
		if _key[0] == 305 and 305 in self.keyboard_down_array:
			self.keyboard_down_array.remove(305)

	# 通用的按键事件
	def key_process_normal(self, _from_target, _key):
		if _key[0] == 99 and 305 in self.keyboard_down_array:
			# "ctrl+c"
			_from_target.target.copy()
		elif _key[0] == 118 and 305 in self.keyboard_down_array:
			# "ctrl+v"
			_from_target.target.paste()
		elif _key[0] == 97 and 305 in self.keyboard_down_array:
			# "ctrl+a"
			_from_target.target.select_all()
		elif _key[0] == 112 and 305 in self.keyboard_down_array:
			# "ctrl+z"
			_from_target.target.do_undo()
		elif _key[0] == 112 and 305 in self.keyboard_down_array:
			# "ctrl+z"
			_from_target.target.do_undo()
		elif _key[0] == 121 and 305 in self.keyboard_down_array:
			# "ctrl+y"
			_from_target.target.do_redo()
		elif _key[0] == 120 and 305 in self.keyboard_down_array:
			# "ctrl+x"
			_from_target.target.cut()
		elif _key[0] == 8:
			# "backspace"
			_from_target.target.do_backspace()
		elif _key[0] == 127:
			# "del"
			_from_target.target.delete_selection()
		elif _key[0] == 276:
			# "left"
			_from_target.target.do_cursor_movement('cursor_left')
		elif _key[0] == 275:
			# "right"
			_from_target.target.do_cursor_movement('cursor_right')
		elif _key[0] == 273:
			# "up"
			_from_target.target.do_cursor_movement('cursor_up')
		elif _key[0] == 274:
			# "down"
			_from_target.target.do_cursor_movement('cursor_down')
		elif _key[0] == 278:
			# "home"
			_from_target.target.do_cursor_movement('cursor_home')
		elif _key[0] == 279:
			# "end"
			_from_target.target.do_cursor_movement('cursor_end')


	def itchat_start(self):
		itchat_kivy.start(self)

		# 图片展示采用定时器读取 img_download_task，每隔10秒查询一次
		# Clock.schedule_interval(partial(self.img_receive, self.img_download_task), 10)


	def exit_check(self,  *args):

		_box_btn = BoxLayout()
		_btn_back = Button(text='no')
		_btn_exit = Button(text='yes')
		_box_btn.add_widget(_btn_exit)
		_box_btn.add_widget(_btn_back)

		_box = BoxLayout(orientation='vertical')
		_label = Label(text='exit now?')
		_box.add_widget(_label)
		_box.add_widget(_box_btn)

		_popup = Popup(title='check',content=_box)
		_popup.open()
		_btn_back.bind(on_press=_popup.dismiss)
		_btn_exit.bind(on_press=self.close_window)
		return True


	def close_window(self, *args):
		Window.close()




class cmcckv(App):
	def build(self):
		Window.size = (1080, 860)
		return KivyWindow()


if __name__ == "__main__":
		cmcckv().run()



"""
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
	
"""