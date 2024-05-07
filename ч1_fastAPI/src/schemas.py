from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

class ContactModel(BaseModel):
    firstname: str = Field(max_length=30)
    lastname: str = Field(max_length=30)
    email: EmailStr
    phone_number: str = Field(max_length=15)
    birthday: date

class ContactResponse(ContactModel):
    id: int

    class Config:
        orm_mode = True


# представляє корисні дані запиту для створення нового користувача.
class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)

# визначає представлення бази даних користувача
class UserDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True

# модель відповіді
class UserResponse(BaseModel):
    user: UserDb
    detail: str = "User successfully created"

# изначає відповідь при отриманні токенів доступу для користувача, що пройшов аутентифікацію.
class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
class RequestEmail(BaseModel):
    email: EmailStr
