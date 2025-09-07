from pydantic import BaseModel
from typing import List

class BookBase(BaseModel):
    name:str
    type:str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id:int
    class Config:
        from_attributes=True

class User(BaseModel):
    username:str
    email:str
    bio:str|None = None

class Usercreate(User):
    password:str


class showUser(BaseModel):
    id:int
    username:str
    email:str
    bio:str|None = None
    books: List[Book]=[]
    class Config:
        from_attributes=True



