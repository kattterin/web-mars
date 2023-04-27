from requests import get, post, delete
from pprint import pprint

url = 'http://127.0.0.1:8080/api/v2'
pprint(get(f'{url}/users').json())
pprint(get(f'{url}/users/1').json())
pprint(get(f'{url}/users/999').json())
pprint(get(f'{url}/users/q').json())

print(post(f'{url}/users',
           json={'surname': 'Какой-то'}).json())

print(post(f'{url}/users',  # корректный запрос
           json={"surname": 'Фамилия',
                 "name": 'Имя',
                 "age": 44,
                 "position": 'position',
                 "speciality": 'speciality',
                 "address": 'address',
                 "email": 'test2@email.ru',
                 "password": 345
                 }).json())

print(post(f'{url}/users',  # некорректный запрос (недостаток данных)
           json={'age': 88,
                 'name': 'Вася',
                 'email': "A@gmail.com",
                 'address': 19,
                 'password': 467
                 }).json())

print(delete(f'{url}/users/4').json())  # корректный запрос
