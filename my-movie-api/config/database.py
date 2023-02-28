import os
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#Nombre de base de datos
sqlite_file_name = "../database.sqlite"

#Directorio actual
base_dir = os.path.dirname(os.path.realpath(__file__))

#Directorio de la base de datos
database_url = f"sqlite:///{os.path.join(base_dir,sqlite_file_name)}"

#Motor de la base de datos
engine = create_engine(database_url,echo=True)

#Se debe crear una sesion para conectarse a la base de datos
session = sessionmaker(bind=engine)

#Con esto podemos manipular todas las tablas (Declarative base)
Base = declarative_base()