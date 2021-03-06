from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from database import BaseModel


class Category(BaseModel):
    __tablename__ = "Categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)


class User(BaseModel):
    __tablename__ = "Users"

    login = Column(String(256), primary_key=True)
    password_hash = Column(String(1024))
    first_name = Column(String(256), nullable=False)
    last_name = Column(String(256), nullable=False)
    is_admin = Column(Boolean(), nullable=False)


class Ticket(BaseModel):
    __tablename__ = "Ticket"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(256), nullable=False)
    description = Column(String(1024), nullable=False)
    category_id = Column(Integer, ForeignKey('Categories.id'), nullable=False)
    category = relationship(Category, backref=backref('tickets', lazy=True))
    owner_login = Column(String(256), ForeignKey('Users.login'), nullable=True)
    owner = relationship(User, backref=backref('tickets', lazy=True))
    is_treated = Column(Boolean(), nullable=False)
