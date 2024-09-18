from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from . import schemas, crud, models
from .database import get_db

router = APIRouter()

# Routes pour Admins
@router.post("/admins/", response_model=schemas.AdminInDB)
def create_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    return crud.create_admin(db, admin)

@router.get("/admins/{admin_id}", response_model=schemas.AdminInDB)
def get_admin(admin_id: int, db: Session = Depends(get_db)):
    return crud.get_admin(db, admin_id)

# Routes pour ForumUsers
@router.post("/users/", response_model=schemas.ForumUserInDB)
def create_user(user: schemas.ForumUserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.get("/users/{user_id}", response_model=schemas.ForumUserInDB)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return crud.get_user(db, user_id)

# Routes pour Discussions
@router.post("/discussions/", response_model=schemas.DiscussionInDB)
def create_discussion(discussion: schemas.DiscussionCreate, db: Session = Depends(get_db)):
    return crud.create_discussion(db, discussion)

@router.get("/discussions/{discussion_id}", response_model=schemas.DiscussionInDB)
def get_discussion(discussion_id: int, db: Session = Depends(get_db)):
    return crud.get_discussion(db, discussion_id)

# Routes pour Messages
@router.post("/messages/", response_model=schemas.MessageInDB)
def create_message(message: schemas.MessageCreate, db: Session = Depends(get_db)):
    return crud.create_message(db, message)

@router.get("/messages/{message_id}", response_model=schemas.MessageInDB)
def get_message(message_id: int, db: Session = Depends(get_db)):
    return crud.get_message(db, message_id)

# # Routes pour Profiles
# @router.post("/profiles/", response_model=schemas.ProfileInDB)
# def create_profile(profile: schemas.ProfileCreate, db: Session = Depends(get_db)):
#     return crud.create_profile(db, profile)

# @router.get("/profiles/{profile_id}", response_model=schemas.ProfileInDB)
# def get_profile(profile_id: int, db: Session = Depends(get_db)):
#     return crud.get_profile(db, profile_id)

# Routes pour Students
@router.post("/students/", response_model=schemas.StudentInDB)
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    return crud.create_student(db, student)

@router.get("/students/{student_id}", response_model=schemas.StudentInDB)
def get_student(student_id: int, db: Session = Depends(get_db)):
    return crud.get_student(db, student_id)

# Routes pour Subjects
@router.post("/subjects/", response_model=schemas.SubjectInDB)
def create_subject(subject: schemas.SubjectCreate, db: Session = Depends(get_db)):
    return crud.create_subject(db, subject)

@router.get("/subjects/{subject_id}", response_model=schemas.SubjectInDB)
def get_subject(subject_id: int, db: Session = Depends(get_db)):
    return crud.get_subject(db, subject_id)


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm

from . import auth, schemas, crud
from .database import get_db

router = APIRouter()

@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
