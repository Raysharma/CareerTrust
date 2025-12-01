from pydantic import BaseModel, HttpUrl, EmailStr, Field

class CompanyCreate(BaseModel):
    name: str = Field(min_length=2)
    website: HttpUrl | None = None
    email: EmailStr | None = None

class CompanyResponse(BaseModel):
    id: str
    name: str
    website: str | None
    email: str | None
    is_verified: bool
    trust_score: float = 0.0
