from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import model
from database import engine, SessionLocal
import schema

app = FastAPI()

model.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/blog')
def create(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = model.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog')
def all(db: Session = Depends(get_db)):
    blogs = db.query(model.Blog).all()
    return blogs

@app.get('/blog/{id}')
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(model.Blog).filter(model.Blog.id == id).first()
    return blog

@app.put('/blog/{id}')
def updated(id: int, request: schema.Blog, db: Session = Depends(get_db)):
    db.query(model.Blog).filter(model.Blog.id == id).update({'title': 'updated title'})
    db.commit()
    return {'message': 'updated'}

@app.delete('/blog/{id}')
def destroy(id: int, db: Session = Depends(get_db)):
    db.query(model.Blog).filter(model.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return {'message': 'Deleted'}
