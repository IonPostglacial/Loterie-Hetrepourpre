from dataclasses import dataclass

@dataclass
class Category:
    id: int
    name: str

@dataclass
class User:
    login: str
    password_hash: str
    first_name: str
    last_name: str

@dataclass
class Ticket:
    id: int
    name: str
    description: str
    category: Category
    owner: User