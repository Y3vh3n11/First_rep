from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field

class ContactModel(BaseModel):
    first_name: str =Field(max_length=20)
    last_name: str =Field(max_length=20)
    email: str =Field(max_length=100)
    phone_number: str =Field(max_length=20)
    birthday: date

class ContactResponse(ContactModel):
    id: int
    class Config:
        orm_mode = True