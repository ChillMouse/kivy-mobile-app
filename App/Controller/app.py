from distutils.command.build import build
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
        global urlApi, store, oauthpass, sm
        token = store['account']['token']
        params = {'client_id': oauthpass, 'token': token}
        print(params)
        try:
            res = req.post(f'{urlApi}/token', params)
            json = res.json()
            print(json)
            if type(json) == dict and 'result' in json and json['result'] == True:
                sm.current = 'ProductsScreen'
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
            if type(json) == dict and 'status' in json and json['status'] == 'error':
                response.text = json['text']
            else: response.text = ''
            print(json)
        except req.ConnectionError as err:
            response.text = 'Нет интернета'


class ProductsScreen(MDScreen):
    pass

class LoginScreen(MDScreen):

    def post_auth(self):
        global urlApi, store, oauthpass, sm
        url = f'{urlApi}/auth'
        login = self.ids.login_field.text
        password = self.ids.password_field.text
        response = self.ids.response
        params = {'login': login, 'password': password, 'client_id': oauthpass}

        try:
            res = req.post(url=url, params=params)
            json = res.json()
            print(json)
            if type(json) == dict and 'status' in json and json['status'] == 'success':
                store['account'] = {'token': json['token']}
                sm.current = 'ProductsScreen'
            elif type(json) == dict and json['status'] == 'error':
                response.text = json['text']

        except req.ConnectionError as err:
            response.text = 'Нет интернета'

class EtalinaApp(MDApp):
    def build(self):
        global sm # screen manager

        buildKv = Builder.load_file("App/View/kv/container.kv")
        sm = buildKv
        return buildKv
    def on_start(self):
        global store, oauthpass
        oauthpass = """~(!?:2J`;x%5)Nw>"""
        store = JsonStore('account_info.json')
        if 'account' in store:
            container = Container()
            container.check_token_account()
