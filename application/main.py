from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from application.database import engine
from application.models import Base
from application.routers import admin, user, discussion, message, profile, subject, student, auth

# Crée la base de données et les tables à partir des modèles
Base.metadata.create_all(bind=engine)

# Instancie l'application FastAPI
app = FastAPI()

# Gérer les origines CORS
origins = [
    "*"
    # Ajoute ici toutes les autres origines permises
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclure les différents routeurs pour chaque entité
app.include_router(auth.app, prefix="/auth", tags=["Authentication"])
app.include_router(admin.app, prefix="/admins", tags=["Admins"])
app.include_router(user.app, prefix="/users", tags=["Users"])
app.include_router(discussion.app, prefix="/discussions", tags=["Discussions"])
app.include_router(message.app, prefix="/messages", tags=["Messages"])
app.include_router(profile.app, prefix="/profiles", tags=["Profiles"])
app.include_router(subject.app, prefix="/subjects", tags=["Subjects"])
app.include_router(student.app, prefix="/students", tags=["Students"])

# Route d'accueil pour tester si l'application est en cours d'exécution
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
