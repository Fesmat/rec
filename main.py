from flask import Flask, render_template, send_file, jsonify
from flask_login import login_user, LoginManager, current_user, login_required, logout_user
from werkzeug.utils import redirect
from data import db_session
from data.users import User
from forms.login_user import LoginForm
from forms.register_user import RegisterForm
import logging
from data.posts import Post
from tools import search, user_search

app = Flask(__name__)
app.config['SECRET_KEY'] = '1Aj3sL12J09d43Ksp02A'
login_manager = LoginManager()
login_manager.init_app(app)
logging.debug('Debug')


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return 'That\'s CumImdb'
    return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.login == form.login.data).first()
        if user and user.check_password(form.pwd.data):
            db_sess.close()
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        db_sess.close()
        return render_template('login.html',
                               message="Неверный логин или пароль",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


@app.route('/register', methods=['POST', 'GET'])
def register_user():
    if current_user.is_authenticated:
        return redirect('/')
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = User()
        us = db_sess.query(User).filter(User.login == form.login.data).all()
        if us:
            render_template('register.html', title='User registration', form=form,
                            message="Пользователь с таким логином уже существует")
        else:
            user.login = form.login.data
            if form.pwd.data != form.pwd_sec.data:
                form.pwd_sec.errors = ['Пароли не совпадают']
                return render_template('register.html', title='Registration', form=form)
            user.set_password(form.pwd.data)
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.description = form.description.data
            db_sess.add(user)
            db_sess.commit()
            login_user(user)
            return redirect('/')
    return render_template('register.html', title='Registration', form=form)


@app.route('/profile')
def profile():
    if not current_user.is_authenticated:
        return redirect('/login')
    return render_template('my_page.html')


@app.route('/feed')
def feed():
    if not current_user.is_authenticated:
        return redirect('/login')
    return render_template('feed.html')


@app.route('/search_films')
def search_films():
    if not current_user.is_authenticated:
        return redirect('/login')
    return render_template('search_films.php')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/download/<path:path_to_file>')
def download_image(path_to_file):
    return send_file(path_to_file)


@app.route('/load_films/<film>')
def load_film(film):
    film = ' '.join(film.split('_'))
    return jsonify(search.find_films(film))


@app.route('/film/<film_id>')
@app.route('/film/<film_id>/')
def get_film(film_id):
    if not current_user.is_authenticated:
        return redirect('/login')
    film = search.get_info(film_id)
    return render_template('film.html', film=film)


@app.route('/user/<user_id>')
def render_user(user_id):
    if not current_user.is_authenticated:
        return redirect('/login')
    if int(user_id) == current_user.id:
        return redirect('/profile')
    return render_template('user.html', user=user_search.search_user(int(user_id)))


@app.errorhandler(404)
def error_not_found(error):
    return render_template('error404.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


if __name__ == '__main__':
    db_session.global_init("db/global.db")
    post = Post()
    post.creator_id = "1"
    post.text = "Привет текст первый"
    db_sess = db_session.create_session()
    db_sess.add(post)
    db_sess.commit()
    app.run(port=5000, host='127.0.0.1')
