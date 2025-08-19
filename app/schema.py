from pydantic import BaseModel

class Userdata(BaseModel):
    username: str
    password: str

class login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

class credentials(BaseModel):
    title : str
    url : str
    username : str
    password : str
class Roleupadate(BaseModel):
    new_role: str