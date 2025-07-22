from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app=FastAPI()

@app.get('/')
def query():
    return {'data' : {'this is query parameters'}}

@app.get('/blogs')
def index(limit=10,published :bool = True , sort :Optional[str] = None):
    
    if published:
        return {'data' : f'{limit} published blogs from db'}
    else :
        return{'data' : f'{limit} from db'}