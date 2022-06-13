from kivymd.app import MDApp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.lang import Builder
from kivy.core.window import Window
import requests as req

global urlApi
urlApi = 'http://api.cg10280.tmweb.ru/api/mobile'

class Container(ScreenManager):
    pass

class RegisterScreen(Screen):
    def reg_account(self):
        global urlApi
        login = self.ids.login_field.text
        password = self.ids.password_field.text
        params = {'login': login, 'password': password}
        res = req.post(f'{urlApi}/register', params)
        json = res.json()
        print(type(json))
        if type(json) == 'dict' and json['status'] and json['status'] == 'error':
            self.ids.response.text = 'Ошибка регистрации'
        print(res.json())

class ProductsScreen(Screen):
    pass

class LoginScreen(Screen):
    def get_account(self):
        global urlApi
        login = self.ids.login_field.text
        password = self.ids.password_field.text
        res = req.post(f'{urlApi}/auth', {'login': login, 'password': password})
        json = res.json()
        if type(json) == 'dict' and json['status'] and json['status'] == 'error':
            self.ids.response.text = 'Ошибка в логине или пароле'
        print(res.json())

class EtalinaApp(MDApp):
    def build(self):
        buildKv = Builder.load_file("App/View/kv/container.kv")
        self.icon = "App/View/images/icon.png"
        return buildKv