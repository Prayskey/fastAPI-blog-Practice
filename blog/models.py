# ORM - Object Relational Mapper
# Maps the database tables to classes and objects in code
from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship

# Create a Blog model that inherits from the Base class
class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    # FIXED: Changed "blog" to "blogs" to match the User.blogs variable
    creator = relationship("User", back_populates="blogs") 


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    # This correctly references the Blog.creator variable
    blogs = relationship('Blog', back_populates="creator")
