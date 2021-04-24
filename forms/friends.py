from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField


class FriendsForm(FlaskForm):
    username = StringField('Кирилл Воробьев')
    user_photo = FileField(validators=[FileRequired()])
    unfriend = SubmitField('Удалить из друзей')
    make_friend = SubmitField('Добавить в друзья')
