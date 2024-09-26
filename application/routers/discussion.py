from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from application.database import get_db

app = APIRouter()

# Routes pour Discussions
@app.post("/discussions", response_model=schemas.DiscussionInDB)
def create_discussion(discussion: schemas.DiscussionCreate, db: Session = Depends(get_db)):
    return crud.create_discussion(db, discussion)

@app.get("/discussions", response_model=List)
def get_discussions(db: Session = Depends(get_db)):
    return crud.get_discussions(db)

@app.get("/discussions/{discussion_id}", response_model=dict)
def get_discussion(discussion_id: int, db: Session = Depends(get_db)):
    return crud.get_discussion(db, discussion_id)

@app.delete("/discussions/{discussion_id}", response_model=schemas.DiscussionInDB)
def delete_discussion(discussion_id: int, db: Session = Depends(get_db)):
    return crud.delete_discussion(db, discussion_id)