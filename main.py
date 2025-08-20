from fastapi import FastAPI
from pydantic import BaseModel
#1223344
app = FastAPI()

@app.get('/blog/unpublished')
def unpub():
    return{'data' : 'all the unpublished blogs are here'}

@app.get('/')
def index():    
    return {'data' : {'blog list'}}


@app.get('/blog/{id}')
def show(id : int):
    return{'data' : id} 
