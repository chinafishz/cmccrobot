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



#
#
# class ChatWindow(BoxLayout):
#     orientation= 'vertical'
#
#
# class ChatLabel(Label):
#     markup = True
#     valign = 'middle',
#
#

#
# class KivyOperate(Widget):
#

#

#     # 点击聊天列表后的效果
#     def click_chat_list(self):
#
#         _root=self.parent.parent.parent.parent
#         a = _root.ids.id_chat_scroll.children[0]
#
#
#         _root.ids.id_chat_scroll.remove_widget(a)
#
#
#
#     # 接受微信消息_创建场景
#     def itchat_receive_creat(self):
#         _from_name= 'my'
#         _msg='fffff'
#
#         # a = chat_boxlayout()
#         # a.height = 0
#         # a.size_hint_y = None
#
#
#         b=ToggleButton(id=_from_name,text=_msg,group='cmcc')
#         # a.bind(on_release=itchat_kivy.click_chat_list)
#
#         # self.ids.chat_list.add_widget(a)
#         self.chat_list_height = self.chat_list_height + 80
#
#     def itchat_receive_update(self, _msg):
#
#         font_count = self.ids.id_chat_scroll.children[0].width / 15
#         add_height = 25 * (int(len(_msg) / font_count))
#         self.ids.id_chat_scroll.children[0].add_widget(Label(text=_msg, halign='left',  markup=True, valign='middle',text_size=[self.ids.id_chat_scroll.children[0].width, 25+add_height], height=50.0+add_height))
#         self.ids.id_chat_scroll.children[0].height = self.ids.id_chat_scroll.children[0].height + 50.0 + add_height
#         pass
#
#
#     # 启动itchat
#     # def itchat_start(self):
#     #     itchat_main.kivy_start(self)
#
#

class MemberList_ToggleButton(ToggleButton):
    size_hint = [1, None]


    def aa(self):
        print('1222')

class ScrollClass(ScrollView):
    pass


class BackgroundColor(Widget):
    pass


class LeftWidget(Widget):
    pass


class KivyWindow(Widget):

    # 对话记录
    record = ObjectProperty(Widget)

    # 目前member的数量，动态变化
    member_item_count = NumericProperty(1)

    # 设置左栏member的高度
    member_item_height = NumericProperty(100)

    # member_list当前选择的是那个item
    member_list_current = StringProperty('my')

    def __init__(self, **kwargs):
        super(KivyWindow,self).__init__(**kwargs)

    def add_member_list(self,_name):
        self.member_item_count = self.member_item_count + 1
        _togglebutton = MemberList_ToggleButton(_id=_name, text=_name, height=self.member_item_height, group='cmcc')
        _togglebutton.on_release()
        self.ids.member_list.add_widget(_togglebutton)



    def test(self, _togglebutton_id):
        # _togglebutton_id 用于分辨member_list的对方

        if _togglebutton_id == self.member_list_current:
            return
        else:
            self.member_list_current = _togglebutton_id
            print('1111')

    # 发送健效果
    def itchat_send(self):
        _username = ''
        if self.ids.send_to_name.text != '':
            _name = itchat.search_friends(name=self.ids.send_to_name.text)
            # _chatroom= itchat.get_chatrooms()
            _chatroom = itchat.search_chatrooms(name=self.ids.send_to_name.text)
            # _name_2 = itchat.search_chatrooms(userName=self.ids.send_to_name.text)

            if _name != []:
                _username = _name[0].UserName
            elif _chatroom != []:
                _username = _chatroom[0].UserName
            else:
                self.ids.send_to_name.text = '找不到资料'


        else:
            _username = ''
        itchat.send(self.ids.weixin_textinput.text, toUserName=_username)
        font_count = self.ids.id_chat_scroll.children[0].width / 15
        add_height = 25 * (int(len(self.ids.weixin_textinput.text) / font_count))
        self.ids.id_chat_scroll.children[0].add_widget(
            Label(text=self.ids.weixin_textinput.text + '@' + self.ids.send_to_name.text, markup=True,
                  halign='right', valign='middle',
                  text_size=[self.ids.id_chat_scroll.children[0].width, 25 + add_height],
                  height=50.0 + add_height))
        self.ids.weixin_textinput.text = ''
        self.ids.id_chat_scroll.children[0].height = self.ids.id_chat_scroll.children[
                                                         0].height + 50.0 + add_height

        # _root.ids.my.size_hint=[1,0.5]
    # 初始化左栏增加my的对话框
    # chat_window = ChatWindow(id='my')

    # 创建专用的对话窗口组件

    # _root.record.add_widget(chat_window)
    # 增加到记录里面
    # _root.ids.chat_scroll.add_widget(chat_window)
    # 增加到中栏
        pass

class cmcckvApp(App):
    def build(self):
        return KivyWindow()


if __name__ == "__main__":
    cmcckvApp().run()

