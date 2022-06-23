from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.uix.popup import Popup
from kivy.uix.widget import Widget
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDTextButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen, CardTransition
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.storage.jsonstore import JsonStore
import requests as req
import random
import string
import base64


global urlApi
urlApi = 'http://api.cg10280.tmweb.ru/api/mobile'

class Container(ScreenManager):
    def exit_from_account(self):
        global store
        if 'account' in store:
            store.delete('account')
            print('Удалено')
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

class MyBackdropFrontLayer():
    pass

class ProductsScreen(MDScreen):
    def on_enter(self):
        self.get_produts()
    def get_produts(self):
        global urlApi, store, oauthpass, sm
        url = f'{urlApi}/getProducts'
        params = {'client_id': oauthpass}
        res = req.get(url, params)
        if res.status_code == 200:
            json = res.json()
            if 'status' in json and json['status'] == 'success':
                count_items = 0
                for prod in json['results']:
                    count_items += 1
                    randomName = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12));
                    with open(f"App/View/images/temp/{randomName}.png", "wb") as fh:
                        fh.write(base64.decodebytes(str.encode(prod['image'])))
                        fh.close()
                        white = (1, 1, 1, 1)
                        gray = (0.52, 0.52, 0.52, 0.3)
                        if count_items % 2 == 1:
                            color = white
                        else:
                            color = gray

                        box = self.ids.this_front.ids.this_box
                        image = Image(source = f'App/View/images/temp/{randomName}.png', size_hint=(1, 1), pos_hint={'center_y': 0.5, 'center_x': 0.5})
                        name = MDLabel(pos_hint={'center_y': 0.5, 'center_x': 0.5}, size_hint=(0.5, 0.5), text=prod['name'], halign='center')
                        count = MDLabel(pos_hint={'center_y': 0.5, 'center_x': 0.5}, size_hint=(0.5, 0.5), text=prod['description'], halign='center')
                        buy = MDLabel(pos_hint={'center_y': 0.5, 'center_x': 0.5}, size_hint=(0.5, 0.5), text=prod['cost'], halign='center')
                        grid = MDGridLayout(pos_hint={'center_y': 0.5, 'center_x': 0.5}, cols=2, rows=2, md_bg_color=color, padding='20dp')
                        grid.add_widget(name)
                        grid.add_widget(image)
                        grid.add_widget(count)
                        grid.add_widget(buy)
                        box.add_widget(grid)

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
            sm.check_token_account()
