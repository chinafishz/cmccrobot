# -*- coding: utf-8 -*-

from kivy.base import runTouchApp
from kivy.lang import Builder
from kivy.factory import Factory as F


class DemoBox(F.ButtonBehavior, F.BoxLayout):
    pass


runTouchApp(Builder.load_string('''


<MyToggleButton@ToggleButton>:
    hacked_state: False
    allow_no_selection: False
    on_state: self.hacked_state = self.state == 'down'
<HalignButton@MyToggleButton>:
    text: 'auto'
    group: 'halign'
    on_hacked_state: for c in root.parent.__boxes.children: \
                c.halign = root.text

<DemoBox>:
    text: ti.text
    language: ''
    halign: 'auto'
    font_size: '20sp'
    font_context: 'system://'
    base_direction: None
    markup: True
    orientation: 'horizontal'
    padding: '5dp'
    spacing: '5dp'
    size_hint_y: None
    height: lbl.texture_size[1] + 25
    on_text:
        if self.text: ti.text = self.text

    
    Label:
        id: lbl
        halign: root.halign
        text: root.text
        markup: root.markup
        font_context: root.font_context != 'None' and \
                      root.font_context or None
        base_direction: root.base_direction != 'None' and \
                        root.base_direction or None
      
  
    TextInput:
        id: ti
        halign: root.halign
        cursor_width: 3
        font_context: root.font_context != 'None' and root.font_context or None
        base_direction: root.base_direction != 'None' and \
                        root.base_direction or None

BoxLayout:
    ScrollView:
        id: sv
      
        BoxLayout:
            id: boxes
          
            DemoBox:
                language: 'Chinese'
                text: '你好，这是中文竖排测试。\\n欢迎来到中国北京。'
           
    # --------------------------------------- HALIGN
    BoxLayout:
        __boxes: boxes
      

        HalignButton:
            text: 'auto'
            state: 'down'
        HalignButton:
            text: 'left'
        HalignButton:
            text: 'center'
        HalignButton:
            text: 'right'

   
'''))