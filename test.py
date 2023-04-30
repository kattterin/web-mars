from requests import get, post, delete
from pprint import pprint

url = 'http://localhost:8080/api'

# pprint(get(f'{url}/users').json()) # Получение всех пользователей
# pprint(get(f'{url}/user/4').json()) # Получение одного пользователя
# print(post(f'{url}/user', json={"id": 444,
#                                 "name": "Test1",  # Добавление пользователя
#                                 "email": "test@gmail.com",
#                                 "surname": "Test2",
#                                 "age": 22,
#                                 "position": "Капитан",
#                                 "speciality": "человек",
#                                 "address": "kanash",
#                                 "password": "1234"
#                                 }).json())

# print(post(f'{url}/user/5', json={"name": "Test7",  # Редактирование пользователя
#                                   "email": "test1@gmail.com",
#                                   "speciality": "человек=2"
#                                   }).json())


print(delete(f'{url}/user/444').json())  # Удаление пользователя



# print(post(f'{url}/job/88',
#            json={}).json())  # пустой json
# print(post(f'{url}/job/8877',
#            json={'work_size': 14}).json())  # работы с id = 8877 нет в базе
# print(post(f'{url}/job/qwe').json())  # некорректное значение id
#
# print(post(f'{url}/job/88',
#            json={'work_size': 16  # все сработало
#                  }).json())

# print(delete(f'{url}/jobs/99999').json())  # работы с id = 999 нет в базе
# print(delete(f'{url}/jobs/qwe').json())  # некорректное значение id
# print(delete(f'{url}/jobs/4').json())  # все работает
# pprint(get(f'{url}/jobs').json())

# pprint(get(f'{url}/jobs').json())
# pprint(get(f'{url}/job/1').json())
# pprint(get(f'{url}/job/999').json())
# pprint(get(f'{url}/job/q').json())

# print(post(f'{url}/jobs',
#            json={}).json())  # пустой json
#
# print(post(f'{url}/jobs',
#            json={'job': 'Заголовок'}).json())  # недостаточно данных
#
# print(post(f'{url}/jobs',
#            json={'id': 1,
#                  'job': 'работа 4',
#                  'team_leader': 2,
#                  'work_size': 19,
#                  'is_finished': False
#                  }).json())  # Работа с такими данными уже есть
#
# print(post(f'{url}/jobs',
#            json={'id': 11,
#                  'job': 'работа 5',
#                  'team_leader': 2,
#                  'work_size': 19,
#                  'is_finished': True  # все сработало
#                  }).json())
#
# pprint(get(f'{url}/jobs').json())
