from requests import get, post, delete
from pprint import pprint

url = 'http://localhost:8080/api'
# pprint(get(f'{url}/jobs').json())
# pprint(get(f'{url}/job/1').json())
# pprint(get(f'{url}/job/999').json())
# pprint(get(f'{url}/job/q').json())

print(post(f'{url}/jobs').json())

print(post(f'{url}/jobs',
           json={'job': 'Заголовок'}).json())

print(post(f'{url}/jobs',
           json={'id': 1,
                 'job': 'работа 4',
                 'team_leader': 2,
                 'work_size': 19,
                 'is_finished': False
                 }).json())

print(post(f'{url}/jobs',
           json={'id': 88,
                 'job': 'работа 4',
                 'team_leader': 2,
                 'work_size': 19,
                 'is_finished': False
                 }).json())
