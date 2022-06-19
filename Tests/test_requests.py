import unittest
import requests as req
# import os, sys
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# # import ../App/
# import App.Controller.app as app

# URL на API
global urlApi
urlApi = 'http://api.cg10280.tmweb.ru/api/mobile'

def post_auth(log, pas): # Отправка данных на сервер
    global urlApi
    url = f'{urlApi}/auth'

    answer = ''
    params = {'login': log, 'password': pas}
    
    try:
        res = req.post(url=url, params=params)
        answer = res

    except req.ConnectionError as err:
        answer = err
    
    return answer

class TestApiMethods(unittest.TestCase):
    def test_connect_to_api(self): # Проверка доступности API
        self.assertEqual(post_auth('test', 'test').status_code, 200)

    def test_auth_success(self): # Попытка входа существующего пользователя
        self.assertEqual(type(post_auth('test', 'test').json()), list)

    def test_auth_empty_field_password(self): # Попытка входа без пароля
        self.assertEqual(post_auth('test', '').json()['text'], 'Не указан логин или пароль')

    def test_auth_empty_field_login(self): # Попытка входа без логин
        self.assertEqual(post_auth('', 'test').json()['text'], 'Не указан логин или пароль')
    
    def test_auth_empty_fields(self): # Попытка входа без логина и пароля
        self.assertEqual(post_auth('', '').json()['text'], 'Не указан логин или пароль')
    
    def test_auth_unknow_user(self): # Попытка входа несуществующего пользователя
        self.assertEqual(post_auth('HSKJDF', '1823781').json()['text'], 'Пользователь не найден')

if __name__ == '__main__': # Запуск тестов
    unittest.main()
