from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
import warnings
import string
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
import threading


Builder.load_string('''

<itchat_kivy>:
	id_chat_label:root.id_chat_label
	cols_minimum:{0:400,1:400,2:400}
	cols:55
	# 左侧栏	
	GridLayout:
		
		rows:2
		
		size_hint_x:0.15
		
		TextInput:
			size_hint_y:0.08

		ScrollClass:
			size_hint_y:0.92
	
			scroll_x:root.userlist_scroll
			BoxLayout:
				
				orientation:'vertical'
				height:900
				Button:
					id:'id_my'
					text:'my'
					
					# on_release:root.userlist_button(self)
				Button:
					id:'id_file'
					text:'file'
					
					# on_release:root.userlist_button(self)
				Button:
				Button:
				Button:
				Button:
				Button:
				Button:
				Button:
				Button:
				Button:
				Button:
				Button:
				Button:
				Button:
					
	BoxLayout:
		size_hint_x:0.85
		orientation:'vertical'
		Label:
			size_hint_y:0.1
			text:'my'
			
		# 对话框
		ScrollClass:
			size_hint_y:0.8
			id:id_chat_scroll
			scroll_y:root.chat_scroll
			BoxLayout:
				
				id:id_chat_label
				height:500
				size_hint_y:None
				Label:
					text:'1111'
		
					text_size:self.parent.width,100
	
		BoxLayout:
			size_hint_y:0.1
			TextInput:
				size_hint_x:0.85
				text:root.send_text
			Button:
				size_hint_x:0.15
				text:'send'
				on_release:root.weixin_send()
			
			
		
	

''')



class ScrollClass(ScrollView):
	pass


class itchat_kivy(GridLayout):
	chat_scroll=NumericProperty(0)
	userlist_scroll=NumericProperty(1)
	send_text=StringProperty('')
	id_chat_label=ObjectProperty(None)
	
	def weixin_send(self):
		self.ids.id_chat_label.add_widget(Label(text=self.send_text, front_size=16,halign='left',text_size=[self.ids.id_chat_label.width,50]))
		

		
	#def userlist_button(self, btn):
#
#		temp=Button(text=btn.text)
#		temp.bind(on_release=self.hh)
#		temp.id=btn.id
#		self.ids.gg.add_widget(temp)
#		self.ids.gg.remove_widget(btn)
#		self.ids.ss.scroll_x=1
#		
		
class SomeApp(App):
    def build(self):
        return itchat_kivy()

SomeApp().run()
	


    

