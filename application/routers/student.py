from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from application.database import get_db

app = APIRouter()

# Routes pour Students
@app.post("/students", response_model=schemas.StudentInDB)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

@app.get("/students/{student_id}", response_model=schemas.StudentInDB)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return crud.get_student(db, student_id)

@app.delete("/students/{student_id}", response_model=schemas.StudentInDB)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    return crud.delete_student(db, student_id)