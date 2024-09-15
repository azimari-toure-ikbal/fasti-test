from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from application.database import get_db

app = APIRouter()

# Routes pour Profiles
@app.post("/profiles/", response_model=schemas.ProfileInDB)
def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
    return crud.create_profile(db, profile)

@app.get("/profiles/{profile_id}", response_model=schemas.ProfileInDB)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    return crud.get_profile(db, profile_id)
