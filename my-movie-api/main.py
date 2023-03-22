from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token, validate_token
from fastapi.security import HTTPBearer
from config.database import engine, Base
from routers.movie import movie_router
from middleware.error_Handler import ErrorHandler
from routers.login import login_router

app = FastAPI()
app.title = "Mi aplicacion con FastApi"
app.version = "0.0.1"

Base.metadata.create_all(bind=engine)
app.include_router(movie_router)
app.include_router(login_router)
app.add_middleware(ErrorHandler)

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

@app.get('/', tags=['home']) #tags= permite cambiar un titulo de una API
def message():
    x = "Leonardo Suarez"   
    return HTMLResponse(f'<h1> Hello world {x}</h1>')


