from data import db_session
from data.users import User


def edit_photo(img, user):
    db_sess = db_session.create_session()
    commit_user = db_sess.query(User).filter(User.id == user.id).first()
    if commit_user:
        img.save(f'db/user_images/avatar{commit_user.id}.jpg')
        commit_user.photo = f'/db/user_images/avatar{commit_user.id}.jpg'
        user.photo = f'/db/user_images/avatar{commit_user.id}.jpg'
        db_sess.commit()
        db_sess.close()
    return
