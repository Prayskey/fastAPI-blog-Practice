# Response schemas are exactly the same as response models. They are used to define the structure of the response data that will be sent back to the client. In this case, we have defined a Blog schema that has two fields: title and body. This schema will be used to validate the data that is sent in the request body when creating a new blog entry, as well as to define the structure of the response data when retrieving blog entries from the database.
from typing import List
from pydantic import BaseModel, Field


class Blog(BaseModel):
    id: int
    title: str
    content: str

class User(BaseModel):
    name: str
    email: str
    password: str = Field(..., max_length=72)


class ShowUser(BaseModel):
    name: str
    email: str
    blogs: List[Blog]

    class Config:
       from_attributes = True

class ShowBlog(Blog):
    id: int
    title: str
    content: str
    creator: ShowUser

    class Config:
        from_attributes = True