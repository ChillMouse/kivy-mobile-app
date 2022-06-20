from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
import requests as req

global urlApi
urlApi = 'http://api.cg10280.tmweb.ru/api/mobile'

class Container(ScreenManager):
    def check_token_account(self):
        global urlApi, store, oauthpass
        token = store['account']['token']
        params = {'client_id': oauthpass, 'token': token}
        print(params)
        try:
            res = req.post(f'{urlApi}/token', params)
            json = res.json()
            print(json)
            if type(json) == dict and 'result' in json and json['result'] == True:
                pass
        except req.ConnectionError as err:
            print('Нет интернета')

class RegisterScreen(MDScreen):
    def reg_account(self):
        global urlApi, oauthpass
        login = self.ids.login_field.text
        password = self.ids.password_field.text
        params = {'login': login, 'password': password, 'client_id': oauthpass}
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


class ProductsScreen(MDScreen):
    pass

class LoginScreen(MDScreen):

    def post_auth(self):
        global urlApi, store, oauthpass
        url = f'{urlApi}/auth'
        login = self.ids.login_field.text
        password = self.ids.password_field.text
        response = self.ids.response
<<<<<<< HEAD
        answer = ''
        params = {'login': login, 'password': password}
=======
        params = {'login': login, 'password': password, 'client_id': oauthpass}

>>>>>>> e71fac0f7b8e28104326fec6ea96c886d27f93fc
        try:
            res = req.post(url=url, params=params)
            json = res.json()
            print(json)
<<<<<<< HEAD
            answer = res
            if type(json) == dict and json['status'] == 'error':
=======
            if type(json) == dict and json['status'] == 'success':
                store['account'] = {'token': json['token']}
                Container.switch_to(ProductsScreen)
            elif type(json) == dict and json['status'] == 'error':
>>>>>>> e71fac0f7b8e28104326fec6ea96c886d27f93fc
                response.text = json['text']

        except req.ConnectionError as err:
            response.text = 'Нет интернета'
<<<<<<< HEAD
            answer = err
        return answer
=======
>>>>>>> e71fac0f7b8e28104326fec6ea96c886d27f93fc

class EtalinaApp(MDApp):
    def build(self):
        buildKv = Builder.load_file("App/View/kv/container.kv")
        self.icon = "App/View/images/icon.png"
        return buildKv
    def on_start(self):
        global store, oauthpass
        oauthpass = """~(!?:2J`;x%5)Nw>"""
        store = JsonStore('account_info.json')
        if 'account' in store:
            Container.check_token_account(self)
