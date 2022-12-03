from app.__init__ import db
from app.models import User

from werkzeug.security import generate_password_hash
from flask_login import login_user


def create_username(request):
    username = request.form['username']
    if len(username) > 3:
        return username
    else:
        return None


def create_password(request, min_password):
    password = request.form['password']
    pwd = request.form['pwd']
    if password == pwd and len(password) >= min_password:
        result = generate_password_hash(password)
        return result
    else:
        return None


def create_email(request):
    email = request.form['email']
    if '@' in email and len(email) > 11:
        return email
    else:
        return None


def signup_user(request):
    username = create_username(request)
    email = create_email(request)
    password = create_password(request, 3)
    if username and email and password is not None:
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=True)
        return True
    else:
        return False
