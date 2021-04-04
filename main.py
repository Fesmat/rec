from flask import Flask
from data import db_session
app = Flask(__name__)
app.config['SECRET_KEY'] = '1Aj3sL12J09d43Ksp02A'


@app.route('/', methods=['GET'])
@app.route('/index', methods=['POST'])
def index():
    return 'Test'


if __name__ == '__main__':
    db_session.global_init("db/global.db")
    app.run(port=8080, host='127.0.0.1')
