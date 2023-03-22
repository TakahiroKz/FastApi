from fastapi import APIRouter
from fastapi import FastAPI, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi.security import HTTPBearer
from config.database import session
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middleware.error_Handler import ErrorHandler
from middleware.jwt_bearer import JWTBearer

movie_router = APIRouter()


class Movie(BaseModel):
    id: Optional[int] = None
    title : str = Field(max_length=50)
    overview : str = Field(min_length=5,max_length=50)
    year : int = Field(le=3000)
    rating : float = Field(ge=1, le=10)
    category : str = Field(min_length=5, max_length=20)

    class Config:
        schema_extra = {
            "example": {
                "id" : 1,
                "title": "Mi pelicula",
                "overview" : "Descripcion de la pelicula",
                "year": 2023,
                "rating" : 10.0,
                "category" : "Acción"
            }
        }


#Retornar todas la peliculas
@movie_router.get('/movies', tags=['movies'],response_model=List[Movie], status_code=200,dependencies=[Depends(JWTBearer())]) #
def get_movies() -> List[Movie]:
    db = session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

#Retornar pelicula filtrada por ID, Validaciones parametros ruta / Path
@movie_router.get('/movies/{id}', tags=['movies'],response_model=Movie,status_code=200)
def get_movie(id:int = Path(ge=1, le=2000))-> Movie :
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=200, content={"message":"No se ha encontrado la pelicula"})
    return JSONResponse(status_code=200,content=jsonable_encoder(result))

#Obtener peliculas filtradas por categoria Validacion parametros Query
@movie_router.get('/movies/',tags=['movies'],response_model=List[Movie],status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.category == category.capitalize()).first()
    if not result:
        return JSONResponse(status_code=200, content={"message":"No se ha encontrado la pelicula"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

#Crear una nueva pelicula
@movie_router.post('/movies',tags=['movies'],response_model=dict,status_code=201)
def create_movie(movie: Movie) -> dict:
    db = session()
    print(movie)
    new_movie = MovieModel(**movie.dict())
    print("Nueva pelicula insertada: ",new_movie)
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201,content={"message":"Se ha registrado la pelicula"})

#Modificar una pelicula
@movie_router.put('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
        return JSONResponse(status_code=404, content={'message':'Pelicula no encontrada'})
    result.title = movie.title
    result.overview = movie.overview
    result.rating = movie.rating
    result.year = movie.year
    result.category = movie.category
    db.commit()            
    return JSONResponse(status_code=200, content={"message":"Se ha modificado la pelicula"})

#Eliminar una pelicula
@movie_router.delete('/movies/{id}',tags=['movies'],response_model=dict,status_code=200) 
def delete_movie(id:int) -> dict:
    db = session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()
    if not result:
            return JSONResponse(status_code=404,content={"message":"No se encontro la pelicula"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message":"Se ha Eliminado la pelicula"})
