# fastApi tags are use to spilt the project end points  into sections in the api docs

from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blog"])
def create_blog(
    request: schemas.Blog, db: Session = Depends(get_db)
):  # Create a new Blog entry in the database using the data from the request
    new_blog = models.Blog(title=request.title, content=request.content, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog", response_model=List[schemas.ShowBlog], tags=["blog"])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()  # Query the database for all Blog entries
    return blogs


@app.get(
    "/blog/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog,
    tags=["blog"],
)
def show(id: int, response: Response, db: Session = Depends(get_db)):
    blog = (
        db.query(models.Blog).filter(models.Blog.id == id).first()
    )  # Query the database for a Blog entry with the specified id
    if not blog:
        # If the Blog entry is not found, set the response status code to 404 and return a detail message
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the id {id} is not available"}

        # Alternate but more efficient method.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blog"])
def destroy(id: int, db: Session = Depends(get_db)):
    # Deletes the post with corresponding ID
    blog = (
        db.query(models.Blog)
        .filter(models.Blog.id == id)
        .delete(synchronize_session=False)
    )
    # Commit changes and delete blog from database. Won't delete if not commited to database.
    if not blog:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    db.commit()
    return {"response": f"Blog with id {id} successfully deleted."}


@app.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blog"])
def update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    # Update the post with corresponding ID
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Blog with the id {id} is not available",
        )
    blog.update({"title": request.title, "content": request.content})
    db.commit()
    return {"response": f"Blog with id {id} successfully updated."}


@app.post("/user", response_model=schemas.ShowUser, tags=["user"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(
        new_user
    )  # Refresh the instance to get the updated data from the database, including the generated id.
    return new_user


@app.get("/user/{id}", response_model=schemas.ShowUser, tags=["user"])
def getUser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )
    return user
