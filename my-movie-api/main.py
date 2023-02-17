from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI()
app.title = "Mi aplicacion con FastApi"
app.version = "0.0.1"

movies=[
        {
            "id": 1,
            "title": "Avatar",
            "overview": "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
            "year": "2009",
            "rating": 7.8,
            "category": "Acción"
        }
]

@app.get('/', tags=['home']) #tags= permite cambiar un titulo de una API

def message():
    x = "Leonardo Suarez"   
    return HTMLResponse(f'<h1> Hello world {x}</h1>')

@app.get('/movies', tags=['movies'])

def get_movies():
    return movies