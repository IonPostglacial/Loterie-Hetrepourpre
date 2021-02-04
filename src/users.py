from model import User
from werkzeug.security import generate_password_hash, check_password_hash


def create(login: str, password: str, first_name: str, last_name: str, is_admin: bool):
    return User(
        login=login,
        password_hash=generate_password_hash(password),
        first_name=first_name,
        last_name=last_name,
        is_admin=is_admin)


def check_credentials(login: str, password: str):
    user = User.query.filter_by(login=login).first()
    if user is not None:
        return check_password_hash(user.password_hash, password)
    else:
        return False