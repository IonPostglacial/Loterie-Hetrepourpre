from model import Category
from model import User
from model import Ticket

from werkzeug.security import generate_password_hash, check_password_hash


def create_categories_table(cursor):
    cursor.execute(
        '''CREATE TABLE categories (
            name text,
            id integer NOT NULL,
            PRIMARY KEY (id)
        );''')

def create_users_table(cursor):
    cursor.execute(
        '''CREATE TABLE users (
            login text NOT NULL,
            pwdhash text NOT NULL,
            first_name text,
            last_name text,
            PRIMARY KEY (login)
        );''')

def create_tickets_table(cursor):
    cursor.execute(
        '''CREATE TABLE tickets (
            category_id integer NOT NULL,
            title text,
            description text,
            owner text,
            id int NOT NULL,
            PRIMARY KEY (id),
            FOREIGN KEY (category_id) REFERENCES categories (id),
            FOREIGN KEY (owner) REFERENCES users (login)
        );''')

def create_tables(cursor):
    create_users_table(cursor)
    create_categories_table(cursor)
    create_tickets_table(cursor)

def get_all_categories(cursor):
    cursor.execute('SELECT name, id FROM categories;')
    while (line := cursor.fetchone()) != None:
        yield Category(name=line[0], id=line[1])

def get_all_users(cursor):
    cursor.execute('SELECT login, pwdhash, first_name, last_name FROM users')
    while (line := cursor.fetchone()) != None:
        yield User(login=line[0], password_hash=line[1], first_name=line[2], last_name=line[3])

def create_user(cursor, login: str, password: str, first_name: str, last_name: str):
    cursor.execute('INSERT INTO Users (login, pwdhash, first_name, last_name) VALUES (?, ?, ?, ?)',
        (login, generate_password_hash(password), first_name, last_name))

def check_credentials(cursor, login: str, password: str):
    cursor.execute('SELECT pwdhash FROM users WHERE login = ?', (login))
    saved_creds = cursor.fetchone()
    if saved_creds is not None:
        return check_password_hash(saved_creds[0], password)
    else:
        return False