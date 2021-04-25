import sqlalchemy
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.Integer,
                              nullable=False)
    pwd = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True, default='/db/user_images/default.jpg')
    number_liked_posts = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    number_own_posts = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)
    friends = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    def set_password(self, password):
        self.pwd = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwd, password)


