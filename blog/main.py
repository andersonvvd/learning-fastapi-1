from fastapi import FastAPI, Depends, status, Response, HTTPException
from pydantic import BaseModel
import blog.schemas as schemas
import blog.models as models
import blog.hashing as hashing
from blog.database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import List
from passlib.context import CryptContext

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/blog", tags = ["blogs"])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags = ["blogs"])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog/{id}", status_code=status.HTTP_200_OK, tags = ["blogs"])
def show_single(id, response:Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not available.")
    return blog


@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags = ["blogs"])
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == int(id))
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not available.")
    blog.delete(synchronize_session=False)
    db.commit()
    return "Done"


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, tags = ["blogs"]) 
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == int(id))
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not available.")
    blog.update(request.dict()) 
    db.commit() 
    return "Update"


pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/user", response_model=schemas.ShowUser, tags = ["users"])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name = request.name, email = request.email, password = hashing.Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{id}", response_model = schemas.ShowUser, tags = ["users"])
def get_user(id:int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == int(id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not available.")
    return user
