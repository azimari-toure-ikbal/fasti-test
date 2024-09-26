from typing import List
from sqlalchemy.orm import Session
from . import models, schemas
from werkzeug.security import generate_password_hash
from sqlalchemy.orm import joinedload

#from models import Admin

# CRUD pour Admins
def create_admin(db: Session, admin: schemas.AdminCreate):
    db_admin = models.Admin(**admin.dict())
    db.add(db_admin)
    db_admin.set_password() 
    db.commit()
    db.refresh(db_admin)
    return db_admin

def get_admin(db: Session, num_admin: str):
    return db.query(models.Admin).filter(models.Admin.num_admin == num_admin).first()

def delete_admin(db: Session, num_admin: str):
    db_admin = db.query(models.Admin).filter(models.Admin.num_admin == num_admin).first()
    if db_admin:
        db.delete(db_admin)
        db.commit()
        return True
    return False

def update_admin(db: Session, num_admin: str, admin_update: schemas.AdminUpdate):
    db_admin= db.query(models.Admin).filter(models.Admin.num_admin == num_admin).first()
    if db_admin:
        for key, value in admin_update.dict(exclude_unset=True).items():
            setattr(db_admin, key, value)
        db.commit()
        db.refresh(db_admin)
        return db_admin
    return None


# CRUD pour ForumUsers
def create_user(db: Session, user: schemas.ForumUserCreate):
    db_user = models.ForumUser(**user.dict())
    db.add(db_user)
    db_user.set_password()
    db.commit()
    db.refresh(db_user)
    return db_user

def get_admin_user(db: Session, email: str):
    return db.query(models.Admin).filter(models.Admin.email == email).first()

def get_forum_user(db: Session, email: str):
    return db.query(models.ForumUser).filter(models.ForumUser.email == email).first()

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.ForumUser).filter(models.ForumUser.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False

def update_user(db: Session, user_id: str, user_update: schemas.ForumUserUpdate):
    db_user = db.query(models.ForumUser).filter(models.ForumUser.id == user_id).first()
    if db_user:
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        return db_user
    return None

# CRUD pour Discussions
def create_discussion(db: Session, discussion: schemas.DiscussionCreate):
    db_discussion = models.Discussion(**discussion.dict())
    db.add(db_discussion)
    db.commit()
    db.refresh(db_discussion)
    return db_discussion

def get_discussions(db: Session):
    discussions = db.query(models.Discussion).join(models.ForumUser).all()
    finalDiscussions = []

    for discussion in discussions:
        user = db.query(models.ForumUser).filter(models.ForumUser.id == discussion.id_utilisateur).first()
        newDiscussion = {
            "id": discussion.id,
            "titre": discussion.titre,
            "sous_titre": discussion.sous_titre,
            "contenu": discussion.contenu,
            "creation": discussion.creation,
            "user": {
                "id": user.id,
                "email": user.email,
                "prenom": user.prenom,
                "nom": user.nom,
                "role": user.role
            }
        }

        finalDiscussions.append(newDiscussion)

    return finalDiscussions

def get_discussion(db: Session, discussion_id: int):
    discussion = db.query(models.Discussion).filter(models.Discussion.id == discussion_id).first()
    messages = db.query(models.Message).filter(models.Message.id_discussion == discussion_id).all()
    author = db.query(models.ForumUser).filter(models.ForumUser.id == discussion.id_utilisateur).first()
    finalMessages = []

    for message in messages:
        user = db.query(models.ForumUser).filter(models.ForumUser.id == message.id_utilisateur).first()
        newMessage = {
            "id": message.id,
            "contenu": message.contenu,
            "creation": message.creation,
            "user": {
                "id": user.id,
                "email": user.email,
                "prenom": user.prenom,
                "nom": user.nom,
                "role": user.role
            }
        }

        finalMessages.append(newMessage)

    return {
        "id": discussion.id,
        "titre": discussion.titre,
        "auteur": author,
        "sous_titre": discussion.sous_titre,
        "contenu": discussion.contenu,
        "creation": discussion.creation,
        "messages": finalMessages
    }


def delete_discussion(db: Session, discussion_id: int):
    db_discussion = db.query(models.Discussion).filter(models.Discussion.id == discussion_id).first()
    if db_discussion:
        db.delete(db_discussion)
        db.commit()
        return True
    return False

# CRUD pour Messages
def create_message(db: Session, message: schemas.MessageCreate):
    db_message = models.Message(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_message(db: Session, message_id: int):
    return db.query(models.Message).filter(models.Message.id == message_id).first()

def delete_message(db: Session, message_id: int):
    db_message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if db_message:
        db.delete(db_message)
        db.commit()
        return True
    return False


# CRUD pour Students
def create_student(db: Session, student: schemas.StudentCreate):
    db_student = models.Student(**student.dict())
    db.add(db_student)
    db_student.set_password()
    db.commit()
    db.refresh(db_student)
    return db_student

def get_student(db: Session, student_id: str):
    return db.query(models.Student).filter(models.Student.num_etu == student_id).first()

def delete_student(db: Session, student_id: str):
    db_student = db.query(models.Student).filter(models.Student.num_etu == student_id).first()
    if db_student:
        db.delete(db_student)
        db.commit()
        return True
    return False

def update_student(db: Session, student_id: str, student_update: schemas.StudentUpdate):
    db_student = db.query(models.Student).filter(models.Student.num_etu == student_id).first()
    if db_student:
        for key, value in student_update.dict(exclude_unset=True).items():
            setattr(db_student, key, value)
        db.commit()
        db.refresh(db_student)
        return db_student
    return None

# CRUD pour Subjects
def create_subject(db: Session, subject: schemas.SubjectCreate, file_path: str):
    subject_data = subject.dict(exclude={'file_data'})
    subject_data['chemin'] = file_path
    db_subject = models.Subject(**subject_data)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

def get_subject(db: Session, subject_id: int):
    return db.query(models.Subject).filter(models.Subject.id == subject_id).first()

def delete_subject(db: Session, subject_id: int):
    db_subject = db.query(models.Subject).filter(models.Subject.id == subject_id).first()
    if db_subject:
        db.delete(db_subject)
        db.commit()
        return True
    return False

