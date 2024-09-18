from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from application.database import get_db

app = APIRouter()

# Routes pour Messages
@app.post("/messages", response_model=schemas.MessageInDB)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db, message)

@app.get("/messages/{message_id}", response_model=schemas.MessageInDB)
def get_message(message_id: int, db: Session = Depends(get_db)):
    return crud.get_message(db, message_id)
