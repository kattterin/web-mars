import datetime
import sqlalchemy
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase


class Jobs(SqlAlchemyBase):
    __tablename__ = 'jobs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))  # руководителя, целое число
    job = sqlalchemy.Column(sqlalchemy.String)  # description описание работы
    work_size = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)  # hours объем работы в часах

    collaborators = sqlalchemy.Column(sqlalchemy.String,  # list of id of participants cписок id участников
                                      nullable=True)

    start_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)  # дата начала
    end_date = sqlalchemy.Column(sqlalchemy.DateTime)  # дата окончания

    is_finished = sqlalchemy.Column(sqlalchemy.BOOLEAN, default=False)  # bool  признак завершения

    user = orm.relationship('User')
