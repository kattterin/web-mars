from data import db_session
# from data.jobs import Jobs
# from data.users import User
#
# db_name = input()
#
# db_session.global_init(db_name)
# session = db_session.create_session()
#
# colonists = session.query(User).filter(User.address == 1).all()
# db_name = input()
# global_init(db_name)
# session = create_session()
#
# colonists = session.query(User).filter(User.address == "module_1").all()
#
# for colonist in colonists:
#     print(colonist)
# for colonist in colonists:
#     print(colonist)
from sqlalchemy import desc
from sqlalchemy.orm import sessionmaker
from data.jobs import Jobs

from data.users import User

db_name = input()  # считываем имя базы данных из консоли

# подключаемся к базе данных
db_session.global_init(db_name)
session = db_session.create_session()

# выполняем запрос и выводим результаты
# jobs = session.query(Jobs).filter(Jobs.collaborators > 1).all()
# for job in jobs:
#     print(job.team_leader)
jobs = session.query(Jobs).order_by(Jobs.collaborators).all()
i = jobs[0].collaborators

for job in jobs:
    if job.collaborators == i:
        user = session.query(User).filter(User.id == job.team_leader).first()
        print(f'{user.name} {user.surname}')
    else:
        break
# for user in users:
#     print(user[0])
# db_name = input()
# global_init(db_name)
# session = create_session()
# jobs = session.query(Jobs).order_by(desc(Jobs.collaborators)).all()
# i = jobs[0].collaborators
#
# for job in jobs:
#     if job.collaborators == i:
#         user = session.query(User).filter(User.id == job.team_leader).first()
#         print(f'{user.name} {user.surname}')
#     else:
#         break
