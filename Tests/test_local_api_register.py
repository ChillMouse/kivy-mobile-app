import unittest
import requests as req
from random import choice
from string import ascii_uppercase

# URL на API
global urlApi
urlApi = 'http://127.0.0.1:8000/api/mobile'

def post_register(log, pas): # Отправка данных на сервер
    global urlApi
    url = f'{urlApi}/register'

    answer = ''
    params = {'login': log, 'password': pas}
    
    try:
        res = req.post(url=url, params=params)
        answer = res

    except req.ConnectionError as err:
        answer = err
    
    return answer
random_login = 'test' + ''.join(choice(ascii_uppercase) for i in range(12))

class TestApiMethods(unittest.TestCase):
    def test_connect_to_api(self): # Проверка доступности API
        self.assertEqual(post_register(None, None).status_code, 200)

    def test_register_len_max(self): # Попытка регистрации нового пользователя
        self.assertEqual(post_register('test'.join(choice(ascii_uppercase) for i in range(12)), 'test').json()['text'], 'Длина логина должна быть меньше 50')

    def test_register_success(self): # Попытка регистрации нового пользователя
        self.assertEqual(type(post_register(random_login, 'test').json()), dict)

    def test_register_empty_field_password(self): # Попытка регистрации без пароля
        self.assertEqual(post_register('test', '').json()['text'], 'Не указан логин или пароль')

    def test_register_empty_field_login(self): # Попытка регистрации без логин
        self.assertEqual(post_register('', 'test').json()['text'], 'Не указан логин или пароль')
    
    def test_register_empty_fields(self): # Попытка регистрации без логина и пароля
        self.assertEqual(post_register('', '').json()['text'], 'Не указан логин или пароль')
    
    def test_register_non_unique_user(self): # Попытка регистрации существующего пользователя
        self.assertEqual(post_register('test', 'test').json()['text'], 'Такой пользователь уже существует')

if __name__ == '__main__': # Запуск тестов
    unittest.main()
