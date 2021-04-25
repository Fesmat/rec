from flask import Flask, render_template, send_file, jsonify, request
from flask_login import login_user, LoginManager, current_user, login_required, logout_user
from flask_restful import abort
from werkzeug.utils import redirect
from data import db_session
from data.users import User
from forms.login_user import LoginForm
from forms.register_user import RegisterForm
import logging
from data.posts import Post
from tools import search, user_search
from handlers.friendly_file import make_friend, get_friends, get_maybe_friends, delete_friend, is_friend
from tools.edit_profile_photo import edit_photo
import time
app = Flask(__name__)
app.config['SECRET_KEY'] = '1Aj3sL12J09d43Ksp02A'
login_manager = LoginManager()
login_manager.init_app(app)
logging.debug('Debug')


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return redirect('/feed')
    return redirect('/login')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
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


@app.route('/profile', methods=['POST', 'GET'])
def profile():
    if not current_user.is_authenticated:
        return redirect('/login')
    if request.method == 'POST':
        edit_photo(request.files['photo'], current_user)
    posts = db_sess.query(Post).filter(Post.creator_id == current_user.id)
    return render_template('my_page.html', posts=posts, friends=get_friends(current_user))


@app.route('/feed')
def feed():
    if not current_user.is_authenticated:
        return redirect('/login')
    return render_template('feed.html')


@app.route('/search_films', methods=['POST', 'GET'])
def search_films():
    if not current_user.is_authenticated:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('search_films.html', type_post=False, inp='')
    return render_template('search_films.html', type_post=True, inp=dict(request.form)['search'])


@app.route('/friends', methods=['POST', 'GET'])
def friends():
    if not current_user.is_authenticated:
        return redirect('/login')
    if request.method == 'POST':
        form = request.form
        args = dict(form)
        user_id = args[list(args.keys())[0]]
        if list(args.keys())[0].startswith('make_friend'):
            make_friend(current_user, int(user_id))
        elif list(args.keys())[0].startswith('unfriend'):
            delete_friend(current_user, int(user_id))
    reload_current_user()
    return render_template('friends.html', friends=get_friends(current_user),
                           may_be_friends=get_maybe_friends(current_user))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route('/download/<path:path_to_file>')
def download_image(path_to_file):
    return send_file(path_to_file)


@app.route('/load_films/<film>/<n>')
def load_film(film, n):
    film = ' '.join(film.split('_'))
    if n.isdigit():
        return jsonify(search.find_films(film, int(n)))
    if n == '*':
        return jsonify(search.find_films(film, -1))
    abort(404)


@app.route('/film/<film_id>')
@app.route('/film/<film_id>/')
def get_film(film_id):
    if not current_user.is_authenticated:
        return redirect('/login')
    film = search.get_info(film_id)
    return render_template('film.html', film=film)


@app.route('/user/<user_id>', methods=['POST', 'GET'])
def render_user(user_id):
    if not current_user.is_authenticated:
        return redirect('/login')
    if int(user_id) == current_user.id:
        return redirect('/profile')
    if request.method == 'POST':
        form = request.form
        args = dict(form)
        user_id = args[list(args.keys())[0]]
        if list(args.keys())[0].startswith('make_friend'):
            make_friend(current_user, int(user_id))
        elif list(args.keys())[0].startswith('unfriend'):
            delete_friend(current_user, int(user_id))
    reload_current_user()
    user = user_search.search_user(int(user_id))
    return render_template('user.html', user=user, is_friend=is_friend(current_user, user))


@app.errorhandler(404)
def error_not_found(error):
    return render_template('error404.html')


@login_manager.user_loader
def load_user(user_id):
    return db_sess.query(User).get(user_id)


def reload_current_user():
    user = load_user(current_user.id)
    login_user(user)


if __name__ == '__main__':
    db_session.global_init("db/global.db")
    db_sess = db_session.create_session()
    app.run(port=5000, host='127.0.0.1')
