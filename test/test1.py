from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget


class Aa(Widget):
    pass


class ccApp(App):
    def build(self):
        return Aa()


ccApp().run()