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


# 对话框背景（灰色）
<BackgroundColor@Widget>
    background_color: 0.5, 0.5, 0.5, 0.5
    canvas.before:
        Color:
            rgba: root.background_color
        Rectangle:
            size: self.size
            pos: self.pos
            

# 主类
<itchat_kivy>:
   
				
                
                
    Widget:
        size: root.width-390,root.height
        pos:195,0
        
        # 对话区的标题
        
        BoxLayout:
            size: root.width-390,30
            pos:195,root.height-35
            Label:
                text:'名称'
                
        # 对话区的输入框                
        BoxLayout:
           
            size: root.width-390,60
            pos:195,0
            TextInput:
                id:weixin_textinput
                size_hint_x:0.85
                text:''
            Button:
                size_hint_x:0.15
                text:'发送'
                on_release:root.weixin_send()
            Button:
                size_hint_x:0.1
                text:'增加聊天框'
                on_release:root.test_list()


        # 对话框
        BackgroundColor:
            size: root.width-390,root.height-110
            pos:195,65
            ScrollClass:
                id:id_chat_scroll
                size: root.width-390,root.height-110
                pos:195,65
                scroll_y:0
                # 每个按钮高度为50
                
                    
    
    Widget:
        size: 190,root.height
        pos:5,0
        BoxLayout:
            size: 190,30
            pos:5,root.height-35
            TextInput:
            
        ScrollClass:
            size: 185,root.height-45
            pos:5,0

            BoxLayout:
                size_hint_y:None
                orientation:'vertical'
				id:cn_list
				# 每个按钮高度为80
				height:800
				Button:
				    text:'step1'
				    on_release:root.step1()
				Button:
				    text:'step2'
				    on_release:root.step2()

''')


class ScrollClass(ScrollView):
    pass

class chat_boxlayout(BoxLayout):

    id='id_chat_label'
    orientation= 'vertical'

class itchat_kivy(Widget):
    chat_label_height = NumericProperty(0)
    def weixin_send(self):
        self.ids.id_chat_scroll.children[0].add_widget(Label(text=self.ids.weixin_textinput.text, markup=True, halign='right',valign='middle', text_size=[self.ids.id_chat_scroll.children[0].width, 25]))
        self.ids.weixin_textinput.text = ''
        self.chat_label_height = self.chat_label_height + 50
        pass

    def step1(self):

        a=chat_boxlayout()
        self.ids.id_chat_scroll.add_widget(a)
        pass

    def step2(self):
        a=self.ids.id_chat_scroll.children[0]
        self.ids.id_chat_scroll.remove_widget(a)
        print('1')
        self.ids.id_chat_scroll.add_widget(a)

    def test_list(self):
        a = Button(id='my', text='my')
        a.bind(on_release=itchat_kivy.btn_test)
        self.ids.cn_list.add_widget(a)

    def btn_test(self):
        print('1')

class SomeApp(App):
    def build(self):
        return itchat_kivy()


SomeApp().run()





