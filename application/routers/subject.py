from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from application.database import get_db

app = APIRouter()

# Routes pour Subjects
@app.post("/subjects", response_model=schemas.SubjectInDB)
async def create_subject(
    title: str = Form(...),
    module: str = Form(...),
    niveau: str = Form(...),
    enseignant: str = Form(...),
    annee_pub: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Save the file and get the path
    file_location = f"files/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(await file.read())

    # Create the subject data dictionary
    subject_data = {
        "title": title,
        "module": module,
        "niveau": niveau,
        "enseignant": enseignant,
        "annee_pub": annee_pub,
        "chemin": file_location,
    }

    # Create the subject in the database
    return crud.create_subject(db, subject_data)

@app.get("/subjects/{subject_id}", response_model=schemas.SubjectInDB)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    return crud.get_subject(db, subject_id)

@app.delete("/subjects/{subject_id}", response_model=schemas.SubjectInDB)
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    return crud.delete_subject(db, subject_id)