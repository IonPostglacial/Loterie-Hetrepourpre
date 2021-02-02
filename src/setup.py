from database import create_tables, create_user

import sqlite3

conn = sqlite3.connect("lottery.sq3")
curs = conn.cursor()

create_tables(curs)

curs.execute("INSERT INTO categories (id, name) VALUES (?, ?)", (1, "Sprite"))
curs.execute("INSERT INTO categories (id, name) VALUES (?, ?)", (2, "Code"))
curs.execute("INSERT INTO categories (id, name) VALUES (?, ?)", (3, "Bruitage"))
curs.execute("INSERT INTO categories (id, name) VALUES (?, ?)", (4, "Musique"))
curs.execute("INSERT INTO categories (id, name) VALUES (?, ?)", (5, "Dialogue"))
curs.execute("INSERT INTO categories (id, name) VALUES (?, ?)", (6, "Fiche Personnage"))

create_user(curs, "pierre", "hello", "Pierre", "Galipot")

curs.close()
conn.commit()
conn.close()