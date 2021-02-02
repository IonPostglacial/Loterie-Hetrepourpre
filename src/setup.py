from database import create_user
from app import db
from model import Category


db.create_all()

db.session.add(Category(id=1, name="Sprite"))
db.session.add(Category(id=2, name="Code"))
db.session.add(Category(id=3, name="Bruitage"))
db.session.add(Category(id=4, name="Musique"))
db.session.add(Category(id=5, name="Dialogue"))
db.session.add(Category(id=6, name="Fiche Personnage"))

db.session.add(create_user("pierre", "hello", "Pierre", "Galipot"))

db.session.commit()