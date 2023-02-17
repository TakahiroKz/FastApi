from fastapi import FastAPI

app = FastAPI()



@app.get('/')

def message():
    x = 4 + 4 
    return "Te amo victoria bb uwu"