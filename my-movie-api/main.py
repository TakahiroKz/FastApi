from fastapi import FastAPI, Body, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional


app = FastAPI()
app.title = "Mi aplicacion con FastApi"
app.version = "0.0.1"

#Esquema para recibir datos.
class Movie(BaseModel):
    id: Optional[int] = None
    title : str = Field(max_length=15)
    overview : str = Field(min_length=5,max_length=50)
    year : str = Field(max_length="4")
    rating : float = Field(ge=1, le=10)
    category : str = Field(min_length=5, max_length=20)

    class Config:
        schema_extra = {
            "example": {
                "id" : 1,
                "title": "Mi pelicula",
                "overview" : "Descripcion de la pelicula",
                "year": "2023",
                "rating" : 10.0,
                "category" : "Acción"
            }
        }

movies=[
    {
        "id": 1,
        "title": "Avatar",
        "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        "year": "2009",
        "rating": 7.8,
        "category": "Acción"
    },
    {
        "id": 2,
        "title": "InterStellar",
        "overview": "Un viaje con un buen e infinito fin",
        "year": "2012",
        "rating": 9.3,
        "category": "Drama"
    }
]
#Retornar mensaje simple
@app.get('/', tags=['home']) #tags= permite cambiar un titulo de una API
def message():
    x = "Leonardo Suarez"   
    return HTMLResponse(f'<h1> Hello world {x}</h1>')

#Retornar todas la pelicular
@app.get('/movies', tags=['movies']) 
def get_movies():
    return movies

#Retornar pelicula filtrada por ID, Validaciones parametros ruta
@app.get('/movies/{id}', tags=['movies'])
def get_movie(id:int = Path(ge=1, le=2000)):
    for item in movies:
        if item["id"] == id:
            return item
        else:
            response = "Pelicula no encontrada"
    return response

#Obtener peliculas filtradas por categoria Validacion parametros Query
@app.get('/movies/',tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15) ):
    #Solucion 2
    """for item in movies:
        if item["category"] == category and item["year"] == year:
            return item""" 
    return [item for item in movies  if item["category"] == category]

#Crear una nueva pelicula
@app.post('/movies',tags=['movies'])
def create_movie(movie: Movie):
    movies.append(movie)
    return movies

#Modificar una pelicula
@app.put('/movies/{id}',tags=['movies'])
def update_movie(id: int, movie: Movie):
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["rating"] = movie.rating
            item["year"] = movie.year
            item["category"] = movie.category
            return item
    return []

#Eliminar una pelicula
@app.delete('/movies/{id}',tags=['movies']) 
def delete_movie(id:int):
    title = ''
    for item in movies:
        if item["id"] == id:
            title = item["title"]
            movies.remove(item)
            return f"Pelicula con titulo:'{title}' eliminada"  
    return "No se encontro ninguna pelicula"
