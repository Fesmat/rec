from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, SubmitField, BooleanField, TextAreaField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired


class RegisterForm(FlaskForm):
    login = EmailField('Логин (почта)', validators=[DataRequired()])
    pwd = PasswordField('Пароль', validators=[DataRequired()])
    pwd_sec = PasswordField('Введите пароль повторно', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    name = StringField('Имя', validators=[DataRequired()])
    age = IntegerField('Возраст', validators=[DataRequired()])
    description = TextAreaField('Введите описание', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Создать')
