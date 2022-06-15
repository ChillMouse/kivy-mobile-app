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
        response = self.ids.response
        try:
            res = req.post(f'{urlApi}/register', params)
            json = res.json()
            if type(json) == dict and json['status'] and json['status'] == 'error':
                response.text = json['text']
            else: response.text = ''
            print(json)
        except req.ConnectionError as err:
            response.text = 'Нет интернета'


class ProductsScreen(Screen):
    pass

class LoginScreen(Screen):
    
    def post_auth(self):
        global urlApi
        url = f'{urlApi}/auth'
        login = self.ids.login_field.text
        password = self.ids.password_field.text
        response = self.ids.response
        params = {'login': login, 'password': password}
        try:
            res = req.post(url=url, params=params)
            json = res.json()
            print(json)
            if type(json) == dict and json['status'] == 'error':
                response.text = json['text']
            else: response.text = ''
        except req.ConnectionError as err:
            response.text = 'Нет интернета'



class EtalinaApp(MDApp):
    def build(self):
        buildKv = Builder.load_file("App/View/kv/container.kv")
        self.icon = "App/View/images/icon.png"
        return buildKv