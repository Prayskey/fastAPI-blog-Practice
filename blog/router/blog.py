from typing import List
from fastapi import APIRouter, Depends, status,  HTTPException
from .. import schemas, database, models
from sqlalchemy.orm import Session

router = APIRouter()

get_db = database.get_db

@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=["blog"])
def create_blog(
    request: schemas.Blog, db: Session = Depends(get_db)
):  # Create a new Blog entry in the database using the data from the request
    new_blog = models.Blog(title=request.title, content=request.content, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/blog", response_model=List[schemas.ShowBlog], tags=["blog"])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()  # Query the database for all Blog entries
    return blogs

@router.get(
    "/blog/{id}",
    status_code=status.HTTP_200_OK,
    response_model=schemas.ShowBlog,
    tags=["blog"],
)
def show(id: int, db: Session = Depends(get_db)):
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

@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["blog"])
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


@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["blog"])
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

