import requests
import json
class APIManager:
    def __init__(self, url):
        self.url = str(url)

    def get(self, url, data=None):
        return requests.get(f'{self.url}{url}', data)

    def post(self, url, data=None, json=None):
        return requests.post(f'{self.url}{url}', data=data, json=json)

api = APIManager('http://api.cg10280.tmweb.ru/api/')

arg = {'login': '123', 'password': '123'}

print(api.get('auth/', arg).text)

arg = {'id_to_user': 1, 'id_from_user': 1, 'text': '123123123'}

print(api.post('newMessage', data=arg))

json.dumps(['foo', {'baz': 123}])


