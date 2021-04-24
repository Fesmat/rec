from random import choices
from data import db_session
from data.users import User


def make_friend(current_user, friend_id):
    db_sess = db_session.create_session()
    print('++++')
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user_to_fr = db_sess.query(User).filter(User.id == friend_id).first()
    if not current_user or not user_to_fr:
        return
    friends = current_user.friends
    if friends:
        friends += f', {friend_id}'
    else:
        friends = str(friend_id)
    user.friends = friends
    print(user.friends)
    db_sess.commit()
    db_sess.close()
    return


def get_friends(current_user):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if not user:
        return
    if user.friends:
        friends = user.friends.split(', ')
        res = []
        for fr in friends:
            res.append(db_sess.query(User).filter(User.id == int(fr)).first())
        return res
    return []


def get_maybe_friends(current_user):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if not user:
        return
    user_friends = user.friends
    if not user_friends:
        user_friends = []
    else:
        user_friends = list(map(int, user_friends.split(', ')))
    users = db_sess.query(User).filter(User.id != current_user.id).filter(User.id.notin_(user_friends)).all()
    return set(choices(users, k=30)) if users else []


def delete_friend(current_user, friend_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    if not user:
        return
    if user.friends:
        friend_id = str(friend_id)
        friends = user.friends.split(', ')
        if friend_id in friends:
            del friends[friends.index(friend_id)]
        user.friends = ', '.join(friends)
        db_sess.commit()
        db_sess.close()
    return
