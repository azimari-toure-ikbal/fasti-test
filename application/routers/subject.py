from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from application.database import get_db

app = APIRouter()

# Routes pour Subjects
@app.post("/subjects", response_model=schemas.SubjectInDB)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db, subject)

@app.get("/subjects/{subject_id}", response_model=schemas.SubjectInDB)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    return crud.get_subject(db, subject_id)
