from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class ContactModel(BaseModel):
    firstname: str = Field(max_length=25)
    lastname: str = Field(max_length=25)
    email: EmailStr
    phone: str
    birthday: datetime
    description: str = Field(max_length=150)


class ContactResponse(BaseModel):
    id: int
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    birthday: datetime
    description: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
