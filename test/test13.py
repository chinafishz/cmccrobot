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
	StackLayout:
        orientation:'rl-bt'
        ToggleButton:
            group:'g'
            text:'2'
        ToggleButton:
            text:'2'
            group:'g'
        ToggleButton:
            text:'3'
''')


class itchat_kivy(Widget):
	pass


class SomeApp(App):
    def build(self):
        return itchat_kivy()

SomeApp().run()
	


    

