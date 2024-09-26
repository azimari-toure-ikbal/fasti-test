from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, Response, Cookie
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from application.schemas import ForumUserInDB, Token
from application.crud import get_admin_user, get_forum_user
from application.database import get_db
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import BaseModel
from werkzeug.security import check_password_hash

# Configuration de la sécurité
SECRET_KEY = "DIT_PROJECT1"  # Remplace par une clé secrète plus forte
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Configuration du contexte de hashage des mots de passe
pwd_context = CryptContext(schemes=["scrypt"], deprecated="auto")

app = APIRouter()

class LoginData(BaseModel):
    email: str
    password: str

# Fonction pour vérifier si le mot de passe fourni correspond au hash stocké
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return check_password_hash(
        hashed_password,
        plain_password,
    )

# Fonction pour authentifier un utilisateur en vérifiant son email et mot de passe
def authenticate_admin(db: Session, email: str, password: str):
    user = get_admin_user(db, email=email)
    if not user:
        return False
    
    if not verify_password(password, user.mdp):
        return False
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = get_forum_user(db, email=email)

    print(f"forum user : {user}")

    if not user:
        return False
    
    if not verify_password(password, user.mdp):
        return False
    return user

# Fonction pour générer un token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@app.post("/auth/admin")
async def admin_login(login_data: LoginData, db: Session = Depends(get_db)):
    user = authenticate_admin(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "nom": user.nom,
        "prenom": user.prenom,
        "email": user.email,
        "role": "ADMIN",
    }

@app.post("/auth/user")
async def user_login(login_data: LoginData, db: Session = Depends(get_db)):
    user = authenticate_user(db, login_data.email, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {
        "id": user.id,
        "nom": user.nom,
        "prenom": user.prenom,
        "email": user.email,
        "role": user.role,
    }

async def get_current_user(user_info: Optional[str] = Cookie(None), db: Session = Depends(get_db)):
    if user_info is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Non authentifié",
        )
    
    user_data = dict(item.split("=") for item in user_info.split(";"))
    
    user = get_user(db, email=user_data.get("email"))
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Utilisateur non trouvé",
        )
    
    return user