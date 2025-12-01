# backend/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Literal

Role = Literal["student", "company", "admin"]

class UserCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=6)
    role: Role = "student"

class UserResponse(BaseModel):
    id: str
    name: str
    email: EmailStr
    role: Role

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
