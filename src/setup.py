from model import Category
from database import engine, LocalSession, BaseModel

import users


db = LocalSession()

BaseModel.metadata.create_all(bind=engine)

db.add(Category(name="Sprite"))
db.add(Category(name="Code"))
db.add(Category(name="Bruitage"))
db.add(Category(name="Musique"))
db.add(Category(name="Dialogue"))
db.add(Category(name="Fiche Personnage"))

db.add(users.create("pierre", "hello", "Pierre", "Galipot", True))

db.commit()
db.close()