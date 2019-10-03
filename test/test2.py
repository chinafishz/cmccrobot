from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout

long_text = 'yay moo cow foo bar moo baa ' * 100

Builder.load_string('''
#:kivy 1.4
<aaa>:
    Button:
    
    <ScrollableLabel>:
        Label:
            text:'123'
    
''')

class ScrollableLabel(ScrollView):
    text = StringProperty('')

class aaa(BoxLayout):
    pass
class ScrollApp(App):
    def build(self):
        return aaa()

if __name__ == "__main__":
    ScrollApp().run()