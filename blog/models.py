# ORM - Object Relational Mapper
# Maps the database tables to classes and objects in code
from sqlalchemy import Column, Integer, String
from .database import Base

# Create a Blog model that inherits from the Base class
class Blog(Base):
  __tablename__ = "blogs"

  id = Column(Integer, primary_key=True, index=True)
  title = Column(String, index=True)
  content = Column(String, index=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)