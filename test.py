from requests import get, post, delete
from pprint import pprint

url = 'http://localhost:8080/api'
pprint(get(f'{url}/jobs').json())
pprint(get(f'{url}/job/1').json())
pprint(get(f'{url}/job/999').json())
pprint(get(f'{url}/job/q').json())

# print(get('http://localhost:8080/api/news').json())
# print(get('http://localhost:8080/api/news/2').json())
# print(get('http://localhost:8080/api/news/q').json())


# print(post('http://localhost:8080/api/news').json())
#
# print(post('http://localhost:8080/api/news',
#            json={'title': 'Заголовок'}).json())
#
# print(post('http://localhost:8080/api/news',
#            json={'title': 'Заголовок',
#                  'content': 'Текст новости',
#                  'user_id': 1,
#                  'is_private': False}).json())

# print(delete('http://localhost:8080/api/news/999').json())
# # новости с id = 999 нет в базе
#
# print(delete('http://localhost:8080/api/news/3').json())
