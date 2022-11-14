from app import db, User
from werkzeug.security import generate_password_hash
from flask_login import login_user


def create_username(username):
    if len(username) > 3:
        return username
    else:
        return None


def create_password(password, password_b, min_password):
    if password == password_b and len(password) > min_password:
        return password
    else:
        return None


def create_email(email):
    if '@' in email and len(email) > 11:
        return email
    else:
        return None


def signup_user(request):
    f_name = request.form['username']
    f_email = request.form['email']
    pwd = request.form['password']
    pwd_2 = request.form['password_b']
    username = create_username(f_name)
    email = create_email(f_email)
    passwd = create_password(pwd, pwd_2, 3)
    if username and email and passwd is not None:
        password = generate_password_hash(passwd)
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return True
    else:
        return False
