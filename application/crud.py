from sqlalchemy.orm import Session
from . import models, schemas
from werkzeug.security import generate_password_hash
from models import Admin

# CRUD pour Admins
def create_admin(db: Session, admin: schemas.AdminCreate):
    db_admin = models.Admin(**admin.dict())
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    db_admin.set_password() 
    return db_admin

def get_admin(db: Session, admin_id: int):
    return db.query(models.Admin).filter(models.Admin.num_admin == admin_id).first()

# CRUD pour ForumUsers
def create_user(db: Session, user: schemas.ForumUserCreate):
    db_user = models.ForumUser(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db_user.set_password()
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.ForumUser).filter(models.ForumUser.id == user_id).first()



# CRUD pour Discussions
def create_discussion(db: Session, discussion: schemas.DiscussionCreate):
    db_discussion = models.Discussion(**discussion.dict())
    db.add(db_discussion)
    db.commit()
    db.refresh(db_discussion)
    return db_discussion

def get_discussion(db: Session, discussion_id: int):
    return db.query(models.Discussion).filter(models.Discussion.id == discussion_id).first()

# CRUD pour Messages
def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message(db: Session, message_id: int):
    return db.query(models.Message).filter(models.Message.id == message_id).first()

# CRUD pour Profiles
def create_profile(db: Session, profile: schemas.ProfileCreate):
    db_profile = models.Profile(**profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

def get_profile(db: Session, profile_id: int):
    return db.query(models.Profile).filter(models.Profile.id == profile_id).first()

# CRUD pour Students
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    db_student.set_password()
    return db_student

def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.num_etu == student_id).first()

# CRUD pour Subjects
def create_subject(db: Session, subject: schemas.SubjectCreate):
    db_subject = models.Subject(**subject.dict())
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.id == subject_id).first()
