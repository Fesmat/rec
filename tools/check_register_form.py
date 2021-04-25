def check_login(login):
    pass


def check_pwd(pwd):
    if len(pwd) < 6:
        return 'Длина пароля не может быть менее 6 символов'
    if len(pwd) > 40:
        return 'Длина пароля не может быть более 40 символов'
    return


def check_name(name):
    if len(name) < 3:
        return 'Имя не может быть длиной менее 3 символов'
    if len(name) > 12:
        return 'Имя не может быть длиной более 12 символов'
    for string in name:
        if not(string.isalpha()):
            return 'Имя должно содержать только строчные символы'
    return


def check_surname(surname):
    if len(surname) < 3:
        return 'Фамилия не может быть длиной менее 3 символов'
    if len(surname) > 12:
        return 'Фамилия не может быть длиной более 12 символов'
    for string in surname:
        if not(string.isalpha()):
            return 'Фамилия должна содержать только строчные символы'
    return


def check_age(age):
    if age < 3:
        return 'Детям до 3 лет нельзя пользоваться нашей сетью (см. Лицензионное соглашение)'
    if age > 130:
        return 'Вы подозрительно старый (просим прощения, если оскорбили)'
    return


def check_description(description):
    if len(description) > 50:
        return 'Описание не может составлять более 50 символов'
    return
