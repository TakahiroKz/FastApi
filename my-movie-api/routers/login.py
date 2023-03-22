from fastapi import APIRouter
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from jwt_manager import create_token, validate_token

login_router = APIRouter()

class user(BaseModel):
    email:str
    password:str

#Retornar mensaje simple

#Autenticacion
@login_router.post('/login', tags=['auth'])
def login(user: user):
    if user.email =="admin@gmail.com" and user.password == "admin":
        token:str = create_token(user.dict())
        return JSONResponse(status_code=200,content=token)
    else:
        return JSONResponse(content="Usuario incorrecto")