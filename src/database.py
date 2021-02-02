from model import Category
from model import User
from model import Ticket
from app import db
from model import User

from werkzeug.security import generate_password_hash, check_password_hash


def create_user(login: str, password: str, first_name: str, last_name: str):
    return User(
        login=login,
        password_hash=generate_password_hash(password),
        first_name=first_name,
        last_name=last_name)

def check_credentials(login: str, password: str):
    user = User.query.filter_by(login=login).first()
    if user is not None:
        return check_password_hash(user.password_hash, password)
    else:
        return False