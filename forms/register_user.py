from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, IntegerField, SubmitField, BooleanField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, ValidationError
from tools.check_register_form import *


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

    def validate_login(self, field):
        if check_login(field.data):
            raise ValidationError(check_login(field.data))

    def validate_pwd(self, field):
        if check_pwd(field.data):
            raise ValidationError(check_pwd(field.data))

    def validate_surname(self, field):
        if check_surname(field.data):
            raise ValidationError(check_surname(field.data))

    def validate_name(self, field):
        if check_name(field.data):
            raise ValidationError(check_name(field.data))

    def validate_age(self, field):
        if check_age(field.data):
            raise ValidationError(check_age(field.data))

    def validate_description(self, field):
        if check_description(field.data):
            raise ValidationError(check_description(field.data))
