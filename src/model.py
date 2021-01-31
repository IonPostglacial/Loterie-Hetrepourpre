from dataclasses import dataclass

@dataclass
class Category:
    id: int
    name: str

@dataclass
class User:
    id: int
    login: str
    password: str
    first_name: str
    last_name: str

@dataclass
class Ticket:
    id: int
    name: str
    description: str
    category: Category
    owner: User