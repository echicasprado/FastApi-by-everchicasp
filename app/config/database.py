import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

#FIXME Investigar como crear la base de datos y sus tablas con el orm

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
DATABASE = os.getenv("DATABASE")
DRIVE = os.getenv("DRIVE")
DATABASE_MANAGER = os.getenv("DATABASE_MANAGER")

DATABASE_URL = f"{DATABASE_MANAGER}://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}?driver={DRIVE}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
