import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
import datetime


class Post(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'posts'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    creator_id = sqlalchemy.Column(sqlalchemy.Integer,
                                   sqlalchemy.ForeignKey("users.id"), nullable=False)

    text = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    creation_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=True, default=datetime.datetime.now)
    user = orm.relation('User')
