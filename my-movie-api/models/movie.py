from config.database import Base
from sqlalchemy import Column, Integer, String, Float

class Movie(Base):
    __tablename__ = "movie" #se usa para indicar que se debe crear una tabla
    id = Column(Integer, primary_key = True)
    title = Column(String)
    overview = Column(String)
    year = Column(Integer)
    rating = Column(Float)
    category = Column(String)