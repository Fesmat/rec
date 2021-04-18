from data import db_session
from data.users import User


def search_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).one()
    return user
