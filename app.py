from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.window import Window

class Container(ScreenManager):
    pass

class ProductsScreen(Screen):
    pass

class LoginScreen(Screen):
    pass

class EtalinaApp(MDApp):
    def build(self):
        Window.size = (320, 540)
        buildKv = Builder.load_file('etalina.kv')
        self.icon = 'View/images/icon.png'
        return buildKv


if __name__ in ('__main__', '__android__'):
    EtalinaApp().run()