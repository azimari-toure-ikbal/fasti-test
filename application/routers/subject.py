import base64
import os
import re
from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from application.database import get_db

app = APIRouter()

# Routes pour Subjects
@app.post("/subjects", response_model=schemas.SubjectInDB)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    file_path = save_file(subject.file_data, subject.title)

    return crud.create_subject(db, subject, file_path)

@app.get("/subjects", response_model=List)
def get_subjects(db: Session = Depends(get_db)):
    return crud.get_subjects(db)

@app.get("/subjects/{subject_id}", response_model=schemas.SubjectInDB)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    return crud.get_subject(db, subject_id)

@app.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int, db: Session = Depends(get_db)):
    return crud.delete_subject(db, subject_id)

def save_file(encoded_data: str, title: str) -> str:
    # Decode the base64 data
    file_data = base64.b64decode(encoded_data)
    
    # Sanitize the title to make it safe for filenames
    safe_title = sanitize_filename(title)
    
    # Generate a unique file name with the title
    filename = f"{safe_title}_{uuid4()}.jpg"  # Adjust the extension as needed
    
    # Set the file path where to save
    file_dir = "uploaded_files"
    os.makedirs(file_dir, exist_ok=True)
    file_path = os.path.join(file_dir, filename)
    
    # Write the file data to the file
    with open(file_path, 'wb') as f:
        f.write(file_data)
    
    return file_path

def sanitize_filename(filename: str) -> str:
    """
    Sanitize the filename by removing or replacing unsafe characters.
    """
    # Remove leading and trailing whitespace
    filename = filename.strip()
    
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    
    # Remove any character that is not alphanumeric, underscore, or hyphen
    filename = re.sub(r'[^A-Za-z0-9_\-]', '', filename)
    
    # Limit the length of the filename
    return filename[:50]  # Adjust the length as needed