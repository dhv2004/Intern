from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app=FastAPI()
class blog(BaseModel):
    title : str
    body : str 
    published : Optional[bool]
    
@app.get('/')
def query():
    return {'data' : {'this is query parameters'}}

@app.get('/blogs')
def index(limit=10,published :bool = True , sort :Optional[str] = None):
    
    if published:
        return {'data' : f'{limit} published blogs from db'}
    else :
        return{'data' : f'{limit} from db'}
# How to access body and use of put function
@app.put('/blog')
def create_blog(request : blog):
    
    return {'data' : f"blog is created with title as {request.title}"}