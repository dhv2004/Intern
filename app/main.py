from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import data, model, schema, Token, hashing
from app.data import engine, sessionLocal, Base
from app.Token import Tokengen  


model.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/moba')
def message()
	return {"message" : "this was added using mobaXterm"}
@app.post('/register')
def register_user(user: schema.Userdata, db: Session = Depends(get_db)):
    try:
        new_user = model.User(
        username=user.username,
        password=hashing.Hash.bcrypt(user.password),
        role = 'user'  
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User registered successfully"}
    except Exception as e:
        print(e)
        return {"message": str(e)}

@app.post('/login')
def login_user(request: schema.login, db: Session = Depends(get_db)):
    user = db.query(model.User).filter(model.User.username == request.username).first()
    if not user:
        return {"message": "User not found"}
    if not hashing.Hash.verify(user.password, request.password) == True:
        return {"message": "Incorrect password"}
    
    access_token = Tokengen.create_access_token(data={"sub": user.username})
    refresh_token = Tokengen.create_refresh_token(data={"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token
    }


@app.post('/credentials')
def create_credentials(
    credential: schema.credentials,
    db: Session = Depends(get_db),
    current_user: schema.TokenData = Depends(Tokengen.get_current_user)  
):
    user = db.query(model.User).filter(model.User.username == current_user.username).first()
    if not user:
        return {"message": "User not found"}

    encrypted_password = hashing.Hash.encrypt_password(credential.password)
    
    new_cred = model.Credentials(
        title=credential.title,
        url=credential.url,
        username=credential.username,
        password=encrypted_password,
        owner_id=user.id   
    )
  
    
    
    db.add(new_cred)
    db.commit()
    db.refresh(new_cred)
    return {"message": "Credentials created successfully"}

from fastapi import HTTPException

@app.get('/credentials')
def get_credentials(
    db: Session = Depends(get_db), 
    current_user: schema.TokenData = Depends(Tokengen.get_current_user)
):
    user = db.query(model.User).filter(model.User.username == current_user.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    credentials = db.query(model.Credentials).filter(model.Credentials.owner_id == user.id).all()

    result = []
    for c in credentials:
        decrypted_pass = hashing.Hash.decrypt_password(c.password)  # type: ignore
        result.append({
            "id": c.id,
            "title": c.title,
            "url": c.url,
            "username": c.username,
            "password": decrypted_pass
        })

    return result

@app.put('/credentials/{id}')
def update(id : int , request : schema.credentials , db: Session = Depends(get_db) ,current_user: schema.TokenData = Depends(Tokengen.get_current_user) ):
    user = db.query(model.User).filter(model.User.username == current_user.username).first()
    if not user:
        return {"message": "User not found"}
    cred = db.query(model.Credentials).filter(model.Credentials.id == id,model.Credentials.owner_id == user.id).first()

    if not cred:
        return {"message": "Credentials not found"}
    cred.title = request.title # type: ignore
    cred.url = request.url  # type: ignore
    cred.username = request.username    # type: ignore
    cred.password = hashing.Hash.encrypt_password(request.password) # type: ignore
    db.commit()
    db.refresh(cred)
    return {"message": "Credentials updated successfully"}

@app.delete('/credentials/{id}')
def delete(id: int , db: Session = Depends(get_db), current_user: schema.TokenData = Depends(Tokengen.get_current_user)):
    user = db.query(model.User).filter(model.User.username == current_user.username).first()
    if not user:        
        return {"message": "User not found"}
    delcred =db.query(model.Credentials).filter(model.Credentials.id == id , model.Credentials.owner_id == user.id).first()
    if not delcred:
        return {"message": "Credentials not found"}
    db.delete(delcred)
    db.commit()
    return {"message": "Credentials deleted successfully"}


@app.get('/users')
def get_users(db: Session = Depends(get_db) , current_user: schema.TokenData = Depends(Tokengen.get_current_user)):
    user = db.query(model.User).filter(model.User.username == current_user.username).first()
    if not user or user.role != "admin" : #type: ignore
        return {"message": "Access denied"}
    
    user = db.query(model.User).all()
    result = [ { "id" : users.id , "username" : users.username , "role" : users.role } for users in user ]
    return result
@app.put('/users/{user_id}/role')
def update_user_role(
    user_id: int,
    request: schema.Roleupadate,
    db: Session = Depends(get_db),
    current_user: schema.TokenData = Depends(Tokengen.get_current_user)
):
   
    admin_user = db.query(model.User).filter(model.User.username == current_user.username,model.User.role == "admin").first()
    
    if not admin_user:
        return {"message": "Access denied. Only admins can update user roles."}

    target_user = db.query(model.User).filter(model.User.id == user_id).first()
    if not target_user:
        return {"message": "User not found"}

    target_user.role = request.new_role.lower() # type: ignore
    db.commit()
    db.refresh(target_user)
    
    return {"message": f"User role updated to {request.new_role}"}
