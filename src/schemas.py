from pydantic import BaseModel, Field, EmailStr
from typing import Optional
#
# class User(BaseModel):
#     login: str=Field(min_length=8, max_length=20)
#     password: str=Field(min_length=8, max_length=20, pattern=r'[A-Za-z\d!#$%^&*]')
#     email: str=Field(min_length=8, max_length=20, pattern=r'^[A-Za-z\d._%+-]+@mail\.com$')
class User(BaseModel):
    login: str
    password: str
    email: Optional[EmailStr] = None
    age: int
    gender: str
    city: str