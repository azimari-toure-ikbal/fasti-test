from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from application import schemas, crud, models
from application.database import get_db

app = APIRouter()

# Routes pour Admins
@app.post("/admins", response_model=schemas.AdminInDB)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    print(admin.dict())
    return crud.create_admin(db, admin)

@app.get("/admins/{admin_id}", response_model=schemas.AdminInDB)
def get_admin(admin_id: int, db: Session = Depends(get_db)):
    return crud.get_admin(db, admin_id)

@app.delete("/admins/{admin_id}", response_model=schemas.AdminInDB)
def delete_admin(admin_id: int, db: Session = Depends(get_db)):
    return crud.delete_admin(db, admin_id)

@app.put("/admins/{admin_id}", response_model=schemas.AdminInDB)
def put_admin(admin_id: int, db: Session = Depends(get_db)):
    return crud.update_admin(db, admin_id)