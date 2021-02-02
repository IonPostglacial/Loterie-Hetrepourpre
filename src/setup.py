from model import Category
from database import engine, LocalSession, BaseModel

import users


db = LocalSession()

BaseModel.metadata.create_all(bind=engine)

db.add(Category(id=1, name="Sprite"))
db.add(Category(id=2, name="Code"))
db.add(Category(id=3, name="Bruitage"))
db.add(Category(id=4, name="Musique"))
db.add(Category(id=5, name="Dialogue"))
db.add(Category(id=6, name="Fiche Personnage"))

db.add(users.create("pierre", "hello", "Pierre", "Galipot"))

db.commit()
db.close()