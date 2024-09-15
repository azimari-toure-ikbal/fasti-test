from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Table, Enum, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
from werkzeug.security import generate_password_hash

# Crée une instance de Base
Base = declarative_base()

# # Table d'association pour la relation Many-to-Many entre Student et Subject
# association_table = Table(
#     'student_subject',
#     Base.metadata,
#     Column('student_id', Integer, ForeignKey('etudiants.num_etu'), primary_key=True),
#     Column('subject_id', Integer, ForeignKey('sujets.id'), primary_key=True)
# )

class Admin(Base):
    __tablename__ = "administrations"
    num_admin = Column(String, unique=True, index=True, nullable=False, primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    mdp = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    nom = Column(String, nullable=False)
    poste = Column(String)
    creation = Column(DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.mdp = generate_password_hash(password)

class ForumUser(Base):
    __tablename__ = "utilisateurs"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    mdp = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    nom = Column(String, nullable=False)
    role = Column(Enum('etudiant', 'moderateur', 'admin', name='user_roles'), nullable=False)
    creation = Column(DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.mdp = generate_password_hash(password)

class Discussion(Base):
    __tablename__ = "discussions"
    id = Column(Integer, primary_key=True, index=True)
    id_utilisateur = Column(Integer, ForeignKey('utilisateurs.id'), nullable=False)
    titre = Column(String, nullable=False)
    sous_titre = Column(String)
    contenu = Column(String, nullable=False)
    creation = Column(DateTime, default=datetime.utcnow)


class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    id_utilisateur = Column(Integer, ForeignKey('utilisateurs.id'), nullable=False)
    id_discussion = Column(Integer, ForeignKey('discussions.id'), nullable=False)
    contenu = Column(String, nullable=False)
    creation = Column(DateTime, default=datetime.utcnow)


class Profile(Base):
    __tablename__ = "profils"
    id = Column(Integer, primary_key=True, index=True)
    num_etu = Column(Integer, ForeignKey('etudiants.num_etu'), nullable=False, unique=True)
    annee_exp = Column(Integer)
    competences = Column(String)
    specialisation = Column(String)
    chemin_cv = Column(String)
    creation = Column(DateTime, default=datetime.utcnow)


class Student(Base):
    __tablename__ = "etudiants"
    num_etu = Column(Integer, primary_key=True, unique=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    mdp = Column(String, nullable=False)
    prenom = Column(String, nullable=False)
    nom = Column(String, nullable=False)
    dob = Column(DateTime, nullable=False)
    niveau = Column(Enum('L1', 'L2', 'M1', 'M2', name='niveau_etudes'), nullable=False)
    creation = Column(DateTime, default=datetime.utcnow)


    def set_password(self, password):
        self.mdp = generate_password_hash(password)

class Subject(Base):
    __tablename__ = "sujets"
    id = Column(Integer, primary_key=True, index=True)
    chemin = Column(String)
    module = Column(String, nullable=False)
    niveau = Column(Enum('L1', 'L2', 'M1', 'M2', name='niveau_etudes'), nullable=False)
    enseignant = Column(String, nullable=False)
    annee_pub = Column(String)
    creation = Column(DateTime, default=datetime.utcnow)

# Configuration du moteur (ici, SQLite)
engine = create_engine("mysql://root:PMzLqbMiFFgbwDHNXTmKVeXFpnsinTTB@autorack.proxy.rlwy.net:12464/railway", echo=True)

# Création des tables dans la base de données
Base.metadata.create_all(engine)

# Création d'une session
Session = sessionmaker(bind=engine)
session = Session()

# Exemple d'ajout d'un étudiant
# new_student = Student(
#     num_etu=1,
#     email='etudiant@example.com',
#     prenom='Jean',
#     nom='Dupont',
#     dob=datetime(2000, 1, 1),
#     niveau='L1'
# )
# new_student.set_password('motdepasse123')

# Ajout d'un sujet
# new_subject = Subject(
#     id=1,
#     module='Mathématiques',
#     niveau='L1',
#     enseignant='Prof. Martin',
#     annee_pub='2024'
# )

# # Lier l'étudiant au sujet
# new_student.subjects.append(new_subject)

# # Ajouter à la session et commit
# session.add(new_student)
# session.add(new_subject)
# session.commit()
