from pydantic import BaseModel

class LoginPass(BaseModel):
    login: str
    password: str

class UserInfo(BaseModel):
    name: str | None
    surname: str | None
    birthdate: str | None
    email: str | None
    phone: str | None
    bio: str | None
