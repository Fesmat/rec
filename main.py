from flask import Flask, render_template
from flask_login import login_user
from werkzeug.utils import redirect

from data import db_session
from data.users import User
from forms.register_user import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '1Aj3sL12J09d43Ksp02A'


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return 'That\'s CumImdb'


@app.route('/login', methods=['POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.password.data):
            db_sess.close()
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        db_sess.close()
        return render_template('login.html',
                               message="Wrong login or password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/register', methods=['POST'])
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        us = db_sess.query(User).filter(User.email == form.email.data).all()
        if us:
            render_template('register.html', title='User registration', form=form,
                            message="Пользователь с таким логином уже существует")
        else:
            user.login = form.loginl.data
            user.set_password(form.pwd.data)
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.liked_films = 0
            user.liked_posts = 0
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
            return redirect('/')
    return render_template('register.html', title='Registration', form=form)


if __name__ == '__main__':
    db_session.global_init("db/global.db")
    app.run(port=5000, host='127.0.0.1')
