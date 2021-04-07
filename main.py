from flask import Flask
from data import db_session

app = Flask(__name__)
app.config['SECRET_KEY'] = '1Aj3sL12J09d43Ksp02A'


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return 'Test'


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            db_sess.close()
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        db_sess.close()
        return render_template('login.html',
                               message="Wrong mail or password",
                               form=form)
    return render_template('login.html', title='Authorization', form=form)


if __name__ == '__main__':
    db_session.global_init("db/global.db")
    app.run(port=8080, host='127.0.0.1')
