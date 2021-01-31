def create_categories_table(cursor):
    cursor.execute(
        '''CREATE TABLE categories (
            name text,
            id int NOT NULL AUTO_INCREMENT,
            PRIMARY KEY (id)
        );''')

def create_users_table(cursor):
    cursor.execute(
        '''CREATE TABLE users (
            login text,
            password text,
            first_name text,
            last_name text,
            PRIMARY KEY (login)
        );''')

def create_tickets_table(cursor):
    cursor.execute(
        '''CREATE TABLE tickets (
            category_id int NOT NULL,
            title text,
            description text,
            owner_id int,
            id int NOT NULL AUTO_INCREMENT,
            PRIMARY KEY (id),
            FOREIGN KEY (category_id) REFERENCES categories (id),
            FOREIGN KEY (owner_id) REFERENCES users (id)
        );''')

def create_tables(cursor):
    create_users_table(cursor)
    create_categories_table(cursor)
    create_tickets_table(cursor)

def get_all_categories(cursor):
    cursor.execute('''SELECT (name, id) FROM categories''')