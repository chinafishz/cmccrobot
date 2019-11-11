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
import warnings
import string
from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
import itchat
import itchat_kivy
import time
from kivy.config import Config
import kivy

# 初始化字体，放在font目录下
kivy.resources.resource_add_path("font/")
cn_font_1 = kivy.resources.resource_find("DroidSansFallback.ttf")


class MemberList_ToggleButton(ToggleButton):
    size_hint = [1, None]


class ScrollClass(ScrollView):
    pass


class BackgroundColor(Widget):
    pass


class LeftWidget(Widget):
    pass


class ChatWindow(BoxLayout):
    orientation = 'vertical'


class ChatLabel(Label):
    markup = True
    valign = 'centre'


class KivyWindow(Widget):
    # 对话记录
    chat_record = {'my': None}

    # 目前member的数量，动态变化
    member_item_count = NumericProperty(1)

    # 设置左栏member的高度
    member_item_height = NumericProperty(100)

    # 设置chat_window的高度
    chat_window_height = NumericProperty(0)

    # member_list当前选择的是那个item
    member_list_current = StringProperty('my')

    # 通讯录
    contact_list = {}

    def __init__(self, **kwargs):
        super(KivyWindow, self).__init__(**kwargs)
        self.ids.chat_scroll.add_widget(StackLayout(orientation='tb-lr', size_hint=[1, None]))

    def add_member_list(self, _id, _name):
        if self.chat_record.get(_id) is not None:

            # 新消息提醒，按钮底色变红
            for i in self.ids.member_list.children:
                if i._id == _id:

                    # 将新消息放在最前 ,children[0]为一个，没考虑永久置顶的因素
                    self.ids.member_list.remove_widget(i)
                    self.ids.member_list.add_widget(i)

                    # 将新消息底色标黄
                    self.ids.member_list.children[0].background_color = [2,2,0,1]
            return
        self.member_item_count = self.member_item_count + 1
        if _id[0:2] == '@@':
            _name = '[群]' + _name
        _togglebutton = MemberList_ToggleButton(_id=_id, text=_name, height=self.member_item_height, group='cmcc', font_name=cn_font_1, background_color = [2,2,0,1])
        _togglebutton.bind(on_release=self.member_list_change)
        self.ids.member_list.add_widget(_togglebutton)

    def member_list_change(self, _togglebutton):
        if _togglebutton._id == self.member_list_current:
            _togglebutton.background_color = [1,1,1,1]
            _togglebutton.state = 'down'
            return
        else:
            _togglebutton.background_color = [1, 1, 1, 1]
            self.record_chat()
            self.member_list_current = _togglebutton._id
            self.read_chat_record()

    # 发送健效果
    def msg_send(self):
        _text = self.ids.weixin_textinput.text
        if _text == '':
            return
        itchat.send(_text, toUserName=self.member_list_current)
        self.show_label('send', _text, self.member_list_current)
        self.ids.weixin_textinput.text = ''

    def msg_receive(self, _id, _text, _name=''):
        if _name != '':
            _name = _name + ': '
        self.show_label('receive', _name + _text, _id)

    def img_receive(self, _id, img_path, _name=''):
        if _name != '':
            _name = _name + ': '
        self.show_img('receive', img_path, _id)

    def record_chat(self):
        self.chat_record.update({self.member_list_current: self.ids.chat_scroll.children[0]})

    def read_chat_record(self):
        # this time member_list_current is chang to new usename
        _new_chat_record = self.chat_record.setdefault(self.member_list_current, None)
        _now_chat_widget = self.ids.chat_scroll.children[0]
        self.ids.chat_scroll.remove_widget(_now_chat_widget)

        if _new_chat_record is None:
            self.chat_window_height = 30
            self.ids.chat_scroll.add_widget(StackLayout(orientation='tb-lr', size_hint=[1, None]))
        else:
            self.chat_window_height = _new_chat_record.height
            self.ids.chat_scroll.add_widget(_new_chat_record)

    # 展示图片
    def show_img(self, _type, _img_path, _chat_window_id='my'):
        _chat_window = None
        _chat_scroll = self.ids.chat_scroll

        if _chat_window_id == self.member_list_current:
            _chat_window = _chat_scroll.children[0]
        else:
            _chat_window = self.chat_record.setdefault(_chat_window_id, None)
            if _chat_window is None:
                _chat_window = StackLayout(orientation='tb-lr', size_hint=[1, None])
                _chat_window.width = _chat_scroll.width
                _chat_window.height = 0
        _label_left = Label()

        _label_main = Image(source=_img_path)
        # _label_main.bind(on_touch_down=self.test)
        _label_main.texture_size= [_label_main.norm_image_size[0], _label_main.norm_image_size[1]]
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
            _chat_scroll.scroll_y = 0
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

        if _chat_window_id == self.member_list_current:
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
            _chat_scroll.scroll_y = 0
            self.chat_window_height = self.chat_window_height + _box.height
            _chat_window.height = self.chat_window_height
        else:
            _chat_window.height = _chat_window.height + _box.height
            self.chat_record.update({_chat_window_id: _chat_window})
        pass

    def itchat_start(self):
        itchat_kivy.start(self)

    def send_pic(self):
        self.show_img('receive', 'client/191110-200000.png', )



class cmcckv(App):
    def build(self):
        return KivyWindow()


if __name__ == "__main__":
    cmcckv().run()
