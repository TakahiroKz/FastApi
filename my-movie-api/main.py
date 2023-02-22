from fastapi import FastAPI, Body, Path, Query, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer


app = FastAPI()
app.title = "Mi aplicacion con FastApi"
app.version = "0.0.1"

#Esquema para recibir datos.


class JWTBearer(HTTPBearer):
    async def __call__(self, request:Request):
        auth = await super().__call__(request)
        data = validate_token(auth.credentials)
        if data['email'] != "admin@gmail.com":
            raise HTTPException(status_code=403, detail="Credenciales son invalidas")

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

class user(BaseModel):
    email:str
    password:str

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

#Autenticacion
@app.post('/login', tags=['auth'])
def login(user: user):
    if user.email =="admin@gmail.com" and user.password == "admin":
        token:str = create_token(user.dict())
        return JSONResponse(status_code=200,content=token)
    else:
        return JSONResponse(content="Usuario incorrecto")


#Retornar todas la peliculas
@app.get('/movies', tags=['movies'],response_model=List[Movie], status_code=200,dependencies=[Depends(JWTBearer())])
def get_movies() -> List[Movie]:
    return JSONResponse(status_code=200,content=movies)

#Retornar pelicula filtrada por ID, Validaciones parametros ruta / Path
@app.get('/movies/{id}', tags=['movies'],response_model=Movie,status_code=200)
def get_movie(id:int = Path(ge=1, le=2000))-> Movie :
    for item in movies:
        if item["id"] == id:
            return JSONResponse(status_code=200,content=item)
        else:
            response = JSONResponse(status_code=404,content="No se encontro la pelicula")
    return response

#Obtener peliculas filtradas por categoria Validacion parametros Query
@app.get('/movies/',tags=['movies'],response_model=List[Movie],status_code=200)
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)) -> List[Movie]:
    data = [item for item in movies  if item["category"] == category]
    return JSONResponse(status_code=200, content=data)

#Crear una nueva pelicula
@app.post('/movies',tags=['movies'],response_model=dict,status_code=201)
def create_movie(movie: Movie) -> dict:
    movies.append(movie)
    return JSONResponse(status_code=201,content={"message":"Se ha registrado la pelicula"})

#Modificar una pelicula
@app.put('/movies/{id}',tags=['movies'],response_model=dict,status_code=200)
def update_movie(id: int, movie: Movie) -> dict:
    for item in movies:
        if item["id"] == id:
            item["title"] = movie.title
            item["overview"] = movie.overview
            item["rating"] = movie.rating
            item["year"] = movie.year
            item["category"] = movie.category
    return JSONResponse(status_code=200, content={"message":"Se ha modificado la pelicula"})

#Eliminar una pelicula
@app.delete('/movies/{id}',tags=['movies'],response_model=dict,status_code=200) 
def delete_movie(id:int) -> dict:
    for item in movies:
        if item["id"] == id:
            movies.remove(item)
            return JSONResponse(status_code=200, content={"message":"Se ha Eliminado la pelicula"})
    return JSONResponse(status_code=404,content={"message":"No se encontro la pelicula"})
