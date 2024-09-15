from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# Schéma pour Admin
class AdminBase(BaseModel):
    email: str
    prenom: str
    nom: str
    poste: str

class AdminCreate(AdminBase):
    mdp: str

class AdminInDB(AdminBase):
    num_admin: str
    creation: datetime

    class Config:
        orm_mode = True

# Schéma pour ForumUser (utilisateur du forum)
class ForumUserBase(BaseModel):
    email: str
    prenom: str
    nom: str
    role: str

class ForumUserCreate(ForumUserBase):
    mdp: str

class ForumUserInDB(ForumUserBase):
    id: int
    creation: datetime

    class Config:
        orm_mode = True

# Schéma pour Discussion
class DiscussionBase(BaseModel):
    titre: str
    sous_titre: Optional[str] = None
    contenu: str

class DiscussionCreate(DiscussionBase):
    id_utilisateur: int

class DiscussionInDB(DiscussionBase):
    id: int
    creation: datetime

    class Config:
        orm_mode = True

# Schéma pour Message
class MessageBase(BaseModel):
    contenu: str

class MessageCreate(MessageBase):
    id_utilisateur: int
    id_discussion: int

class MessageInDB(MessageBase):
    id: int
    creation: datetime

    class Config:
        orm_mode = True

# Schéma pour Profile
class ProfileBase(BaseModel):
    annee_exp: str
    competences: str
    specialisation: str

class ProfileCreate(ProfileBase):
    num_etu: int

class ProfileInDB(ProfileBase):
    id: int
    creation: datetime

    class Config:
        orm_mode = True

# Schéma pour Student (étudiant)
class StudentBase(BaseModel):
    email: str
    prenom: str
    nom: str
    dob: str
    niveau: str

class StudentCreate(StudentBase):
    mdp: str

class StudentInDB(StudentBase):
    num_etu: int
    creation: datetime

    class Config:
        orm_mode = True

# Schéma pour Subject (sujet)
class SubjectBase(BaseModel):
    chemin: str
    module: str
    niveau: str
    enseignant: str
    annee_pub: str

class SubjectCreate(SubjectBase):
    pass

class SubjectInDB(SubjectBase):
    id: int
    creation: datetime

    class Config:
        orm_mode = True


from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None
