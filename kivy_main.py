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
<KivyWindow>:
    
    # 左栏
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
            
            StackLayout:
                size_hint:None,None
                orientation:'rl-bt'
                id:member_list
                height:600
                pos:0,111
                
                # 每个按钮高度为80
            
                ToggleButton:
                    pos:0,0
                    text:'1'
                ToggleButton:
                    pos:0,111
                    text:'2'

                
    # 中栏                
    Widget:
        size: root.width-390,root.height
        pos:195,0
        
        # 对话区的标题
        BoxLayout:
            size: root.width-390,30
            pos:195,root.height-35
            Label:
                text:'名称'
                
        # 对话框
        BackgroundColor:
            size: root.width-390,root.height-110
            pos:195,65
            ScrollClass:
                id:chat_scroll
                size: root.width-390,root.height-110
                pos:195,65
                scroll_y:0
                # 每个按钮高度为50
                
                
        # 对话区的输入框                
        BoxLayout:
            size: root.width-390,30
            pos:195,30
            TextInput:
                id:to_username
                # 输入收信息的人
                
                size_hint_x:0.4
                text:''
            Button:
                size_hint_x:0.2
                text:'发送'
                on_release:root.chat_send()
            Button:
                size_hint_x:0.25
                text:'增加聊天框'
                on_release:root.chat_receive_creat()
            Button:
                size_hint_x:0.25
                text:'更新聊天框'
                on_release:root.chat_receive_update()
            Button:
                size_hint_x:0.25
                text:'启动itchat'
                on_release:root.itchat_start()    
        
        TextInput:
            id:weixin_textinput
            size: root.width-390,30
            pos:195,0



''')


class ScrollClass(ScrollView):
    pass


class KivyWindow(Widget):
    operate = ObjectProperty(None)
    record = ObjectProperty(Widget)
    member_list_height = NumericProperty(260)


class ChatWindow(BoxLayout):
    orientation= 'vertical'


class ChatLabel(Label):
    markup = True
    valign = 'middle',


class MemberList_ToggleButton(ToggleButton):
    pass


class KivyOperate(Widget):
    chat_window_height = NumericProperty(0)


    def init(self,_root):
        a=MemberList_ToggleButton(text='my')
        b = MemberList_ToggleButton(text='you')
        _root.ids.member_list.add_widget(a)
        _root.ids.member_list.add_widget(b)
        # 初始化左栏增加my的对话框

        chat_window = ChatWindow(id='my', height=self.chat_window_height)
        # 创建专用的对话窗口组件
        # _root.record.add_widget(chat_window)
        # 增加到记录里面
        _root.ids.chat_scroll.add_widget(chat_window)
        # 增加到中栏


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


        _root.ids.id_chat_scroll.remove_widget(a)



    # 接受微信消息_创建场景
    def itchat_receive_creat(self):
        _from_name= 'my'
        _msg='fffff'

        # a = chat_boxlayout()
        # a.height = 0
        # a.size_hint_y = None


        b=ToggleButton(id=_from_name,text=_msg,group='cmcc')
        # a.bind(on_release=itchat_kivy.click_chat_list)

        # self.ids.chat_list.add_widget(a)
        self.chat_list_height = self.chat_list_height + 80

    def itchat_receive_update(self, _msg):

        font_count = self.ids.id_chat_scroll.children[0].width / 15
        add_height = 25 * (int(len(_msg) / font_count))
        self.ids.id_chat_scroll.children[0].add_widget(Label(text=_msg, halign='left',  markup=True, valign='middle',text_size=[self.ids.id_chat_scroll.children[0].width, 25+add_height], height=50.0+add_height))
        self.ids.id_chat_scroll.children[0].height = self.ids.id_chat_scroll.children[0].height + 50.0 + add_height
        pass


    # 启动itchat
    # def itchat_start(self):
    #     itchat_main.kivy_start(self)







class SomeApp(App):
    def build(self):

        kivy_window = KivyWindow()
        # 创建根窗口

        kivy_window.operate = KivyOperate()

        kivy_window.operate.init(kivy_window)
        # 初始化根窗口





        return kivy_window


if __name__ == "__main__":
    SomeApp().run()