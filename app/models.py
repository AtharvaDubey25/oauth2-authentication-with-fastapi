from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'   

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    bio = Column(String, nullable=True)

    books = relationship("Book", back_populates="owner")


class Book(Base):   
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    type = Column(String)
    owner_id = Column(Integer, ForeignKey('users.id'))  
    owner = relationship('User', back_populates='books')
