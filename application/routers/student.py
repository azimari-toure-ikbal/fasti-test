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

@app.get("/students", response_model=List[schemas.StudentInDB])
def get_students(db: Session = Depends(get_db)):
    return crud.get_students(db)

@app.get("/students/{num_etu}", response_model=schemas.StudentInDB)
def get_student(num_etu: str, db: Session = Depends(get_db)):
    return crud.get_student(db, num_etu)

@app.delete("/students/{num_etu}", response_model=bool)
def delete_student(num_etu: str, db: Session = Depends(get_db)):
    return crud.delete_student(db, num_etu)

@app.put("/students/{num_etu}", response_model=schemas.StudentInDB)
def put_student(num_etu: str, db: Session = Depends(get_db)):
    return crud.update_student(db, num_etu)