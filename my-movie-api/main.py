from fastapi import FastAPI, Body
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

#Retornar pelicula filtrada por ID
@app.get('/movies/{id}', tags=['movies'])
def get_movie(id:int):
    for item in movies:
        if item["id"] == id:
            return item
        else:
            response = "Pelicula no encontrada"
    return response

#Obtener peliculas filtradas por categoria
@app.get('/movies/',tags=['movies'])
def get_movies_by_category(category: str, year:str):
    #Solucion 2
    """for item in movies:
        if item["category"] == category and item["year"] == year:
            return item""" 
    return [item for item in movies  if item["category"] == category and item["year"] == year]

#Crear una nueva pelicula
@app.post('/movies',tags=['movies'])
def create_movie(id:int = Body(), title:str = Body(),overview:str= Body(),year:str = Body(),rating:float = Body(),category:str = Body()):
    movies.append({
        "id": id,
        "title:":title,
        "overview":overview,
        "year":year,
        "rating":rating,
        "category":category
    })
    return movies

#Modificar una pelicula
@app.put('/movies/{id}',tags=['movies'])
def update_movie(id:int, title:str = Body(),overview:str= Body(),year:str = Body(),rating:float = Body(),category:str = Body()):
    for item in movies:
        if item["id"] == id:
            item["title"] = title
            item["overview"] = overview
            item["rating"] = rating
            item["year"] = year
            item["category"] = category
            return item
    return []

#Eliminar una pelicula
@app.delete('/movies/{id}',tags=['movies']) 
def delete_movie(id:int):
    for item in movies:
        if item["id"] == id:
            title = item["title"]
            movies.remove(item)
    return f"Pelicula con titulo:'{title}' eliminada"  
