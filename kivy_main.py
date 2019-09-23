from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
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
import itchat_main
import itchat


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
        size: 190,root.height
        pos:5,0
        BoxLayout:
            size: 190,30
            pos:5,root.height-35
            TextInput:
            
        # 左栏
        ScrollClass:
            size: 185,root.height-45
            pos:5,0

            StackLayout:
                size_hint_y:None
                orientation:'bt-lr'
                id:chat_list
                
				# 每个按钮高度为80
				height:root.chat_list_height
			

   
                
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
           
            size: root.width-390,30
            pos:195,30
            TextInput:
                id:send_to_name
                size_hint_x:0.4
                text:''
            Button:
                size_hint_x:0.2
                text:'发送'
                on_release:root.itchat_send()
            Button:
                size_hint_x:0.25
                text:'增加聊天框'
                on_release:root.itchat_receive_creat()
            Button:
                size_hint_x:0.25
                text:'更新聊天框'
                on_release:root.itchat_receive_update()
            Button:
                size_hint_x:0.25
                text:'启动itchat'
                on_release:root.itchat_start()    
        
        TextInput:
            id:weixin_textinput
            size: root.width-390,30
            pos:195,0

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
              
                    


''')


class ScrollClass(ScrollView):
    pass



class chat_boxlayout(BoxLayout):
    orientation= 'vertical'


class Chat_Main_Obj(Widget):

    pass


class chat_label(Label):
    markup = True
    halign = 'right'
    valign = 'middle',


class itchat_kivy(Widget):
    chat_label_height = NumericProperty(0)
    chat_list_height = NumericProperty(80)

    # 初始化所有对话的存储对象chat_main_obj
    chat_main_obj = Chat_Main_Obj()

    # 初始化my的对话boxlayout
    temp_boxlayout = chat_boxlayout()
    temp_boxlayout.id = 'my'
    chat_main_obj.add_widget(temp_boxlayout)

    # 发送健效果
    def itchat_send(self):
        _username=''
        if self.ids.send_to_name.text != '':
            _name =itchat.search_friends(name=self.ids.send_to_name.text)
            # _chatroom= itchat.get_chatrooms()
            _chatroom= itchat.search_chatrooms(name=self.ids.send_to_name.text)
            # _name_2 = itchat.search_chatrooms(userName=self.ids.send_to_name.text)

            if _name != []:
                _username = _name[0].UserName
            elif _chatroom != []:
                _username = _chatroom[0].UserName
            else:
                self.ids.send_to_name.text = '找不到资料'


        else:
            _username = ''
        itchat.send(self.ids.weixin_textinput.text, toUserName= _username)
        font_count=self.ids.id_chat_scroll.children[0].width/15
        add_height=25*(int(len(self.ids.weixin_textinput.text)/font_count))
        self.ids.id_chat_scroll.children[0].add_widget(Label(text=self.ids.weixin_textinput.text+'@'+self.ids.send_to_name.text, markup=True, halign='right', valign='middle',text_size=[self.ids.id_chat_scroll.children[0].width, 25+add_height], height=50.0+add_height))
        self.ids.weixin_textinput.text = ''
        self.ids.id_chat_scroll.children[0].height = self.ids.id_chat_scroll.children[0].height + 50.0 + add_height

    # 点击聊天列表后的效果
    def click_chat_list(self):

        _root=self.parent.parent.parent.parent
        a = _root.ids.id_chat_scroll.children[0]
        b = chat_boxlayout()

        _root.ids.id_chat_scroll.remove_widget(a)
        _root.ids.id_chat_scroll.add_widget(b)


    # 接受微信消息_创建场景
    def itchat_receive_creat(self):
        _from_name= 'my'
        _msg='fffff'

        a = chat_boxlayout()
        a.height = 0
        a.size_hint_y = None


        b=ToggleButton(id=_from_name,text=_msg,group='cmcc')
        a.bind(on_release=itchat_kivy.click_chat_list)

        self.ids.chat_list.add_widget(a)
        self.chat_list_height = self.chat_list_height + 80

    def itchat_receive_update(self, _msg):

        font_count = self.ids.id_chat_scroll.children[0].width / 15
        add_height = 25 * (int(len(_msg) / font_count))
        self.ids.id_chat_scroll.children[0].add_widget(Label(text=_msg, halign='left',  markup=True, valign='middle',text_size=[self.ids.id_chat_scroll.children[0].width, 25+add_height], height=50.0+add_height))
        self.ids.id_chat_scroll.children[0].height = self.ids.id_chat_scroll.children[0].height + 50.0 + add_height
        pass


    # 启动itchat
    def itchat_start(self):
        itchat_main.kivy_start(self)







class SomeApp(App):
    def build(self):
        cn_main=itchat_kivy()

        # 原KV文件没有包含，通过代码实现
        a = chat_boxlayout()
        a.height =0
        a.size_hint_y = None
        cn_main.ids.id_chat_scroll.add_widget(a)

        b = ToggleButton(id='my',text='自己',state='down',group='cmcc')
        cn_main.ids.chat_list.add_widget(b)



        return cn_main


if __name__ == "__main__":
    SomeApp().run()