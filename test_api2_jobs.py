from requests import get, post, delete
from pprint import pprint

url = 'http://127.0.0.1:8080/api/v2'
pprint(get(f'{url}/jobs').json())  # список все работ

pprint(get(f'{url}/jobs/3').json())  # корректный запрос
pprint(get(f'{url}/jobs/999').json())  # данной работы нет
pprint(get(f'{url}/jobs/q').json())  # некорректное значение id

print(delete(f'{url}/jobs/4').json())  # корректный запрос

print(post(f'{url}/jobs',
           json={'job': 'Какой-то'}).json()) # недостаток данных

print(post(f'{url}/jobs',
           json={'job': 'работа 5',
                 'team_leader': 2,
                 'work_size': 19,
                 'is_finished': False,
                 "collaborators": '1, 34, 6',
                 }).json())  # корректный запрос

print(post(f'{url}/jobs',
           json={'team_leader': 2,
                 'work_size': 19,
                 'is_finished': False,
                 "collaborators": '1, 34, 6'
                 }).json())  # Отсутствует обязательный аргумент "job"

print(post(f'{url}/jobs',
           json={'job': 'работа 55',
                 'team_leader': 2}).json())  # Отсутствует обязательный аргумент "work_size"
