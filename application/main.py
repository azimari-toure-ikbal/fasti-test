from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import RequestValidationError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from application.database import engine
from application.models import Base
from application.routers import admin, user, discussion, message, subject, student, auth

# Crée la base de données et les tables à partir des modèles
Base.metadata.create_all(bind=engine)

# Instancie l'application FastAPI
app = FastAPI()

origins = [
    "https://azimari-toure-ikbal.github.io",
    "https://azimari-toure-ikbal.github.io/faby_front",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    headers = dict(getattr(exc, "headers", {}))
    headers["Access-Control-Allow-Origin"] = "*"
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers=headers,
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    headers = {"Access-Control-Allow-Origin": "*"}
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
        headers=headers,
    )

@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    headers = {"Access-Control-Allow-Origin": "*"}
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
        headers=headers,
    )

# Inclure les différents routeurs pour chaque entité
app.include_router(auth.app, tags=["Authentication"])
app.include_router(admin.app, tags=["Admins"])
app.include_router(user.app, tags=["Users"])
app.include_router(discussion.app, tags=["Discussions"])
app.include_router(message.app, tags=["Messages"])
#app.include_router(profile.app, prefix="/profiles", tags=["Profiles"])
app.include_router(subject.app, tags=["Subjects"])
app.include_router(student.app, tags=["Students"])

# Route d'accueil pour tester si l'application est en cours d'exécution
@app.get("/")
def read_root():
    return {"message": "Welcome to the DIT application!"}
