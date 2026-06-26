from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models, hashing
from sqlalchemy.orm import Session

router = APIRouter()
get_db = database.get_db
@router.post("/user", response_model=schemas.ShowUser, tags=["user"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(
        name=request.name, email=request.email, password=hashing.Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(
        new_user
    )  # Refresh the instance to get the updated data from the database, including the generated id.
    return new_user


@router.get("/user/{id}", response_model=schemas.ShowUser, tags=["user"])
def getUser(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with the id {id} is not available",
        )
    return user
