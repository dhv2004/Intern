from sqlalchemy import Column, Integer, String , ForeignKey
from app.data import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default='user')  

class Credentials(Base):
    __tablename__ = 'credentials'
    
    id = Column(Integer, primary_key=True, index=True)  
    title = Column(String, index=True)
    url = Column(String, index=True)
    username = Column(String, index=True)
    password = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))  
