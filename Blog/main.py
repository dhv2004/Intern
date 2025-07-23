from fastapi import FastAPI , Depends
import schemas
from sqlalchemy.orm import Session 
import models  
from database import engine , SessionLocal

app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()

@app.post('/blog')
def create(request : schemas.Blog , db : Session= Depends(get_db)):
    new_blog = models.Blog(title=request.title , body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def all (db : Session= Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def show(id: int, db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog 
@app.put('/blog/{id}')
def updated(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).update({'title': 'updated title'})
    db.commit()
    return 'updated'

@app.delete('/blog/{id}' )
def destroy(id: int, db : Session= Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'Done'}
