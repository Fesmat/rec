from random import choices
from data import db_session
from data.users import User


def make_friend(current_user, friend_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == current_user.id).first()
    user_to_fr = db_sess.query(User).filter(User.id == friend_id).first()
    if not current_user or not user_to_fr:
        return
    friends = current_user.friends
    if friends:
        if friend_id in list(map(int, friends.split(', '))):
            return
        friends += f', {friend_id}'
    else:
        friends = str(friend_id)
    user.friends = friends
    db_sess.commit()

    print(is_friend(user, user_to_fr))
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
        if not user.friends:
            user.friends = None
        db_sess.commit()

        print(is_friend(current_user, user))
    return


def is_friend(user1, user2):
    db_sess = db_session.create_session()
    user_one = db_sess.query(User).filter(User.id == user1.id).first()
    user_two = db_sess.query(User).filter(User.id == user2.id).first()
    if user_one.friends and user_two.id in list(map(int, user_one.friends.split(', '))):
        return True
    return False
