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

Builder.load_string('''

<aa>:
	orientation:'vertical'
	Label:
		size_hint_y:0.05
		text:'my'
	ScrolllabelLabel:
		size_hint_y:0.08
		StackLayout:
			id:gg
			width:1500
			size_hint_x:None
			orientation:'rl-bt'
			Button:
				text:'0'
				id:'0'
				on_release:root.hh(self)

	
	ScrolllabelLabel:
		size_hint_y:0.75
		bar_color:[.3,.8,.3,1]
    	Label:
        	text: root.ll
        	font_size: 50
        	text_size: self.width, None
        	size_hint_y: None
        	height: self.texture_size[1]
        	markup:True
        	
	BoxLayout:
		cols:1
		size_hint_y:0.05
		TextInput:
			size_hint_x:0.85
		Button:
			size_hint_x:0.15
			text:'send'
			on_release:root.yy()
''')



class ScrolllabelLabel(ScrollView):
	pass


class aa(BoxLayout):
	ll = StringProperty('ggghh')
	i= NumericProperty(1)

	def yy(self):
		self.ll=self.ll+'\n               u[b]u[/b]j'

		a=Button(text=str(self.i))
		a.bind(on_release=self.hh)
		a.id=str(self.i)
		a.text = str(self.i)
		self.ids.gg.add_widget(a)
		self.i =self.i+1

		
	def hh(self, btn):
		a=self
		temp=Button(text=btn.text)
		temp.bind(on_release=self.hh)
		temp.id=btn.id
		self.ids.gg.add_widget(temp)
		self.ids.gg.remove_widget(btn)
		

class SomeApp(App):
    def build(self):

        return aa()


SomeApp().run()