from pydantic import BaseModel

class LoginPass(BaseModel):
    login: str
    password: str

class UserInfo(BaseModel):
    name: str
    surname: str
    birthdate: str
    email: str
    phone: str
    bio: str