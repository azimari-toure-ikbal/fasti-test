from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from application.database import get_db

app = APIRouter()

# Routes pour ForumUsers
@app.post("/users/", response_model=schemas.ForumUserInDB)
def create_user(user: schemas.ForumUserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@app.get("/users/{user_id}", response_model=schemas.ForumUserInDB)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)
