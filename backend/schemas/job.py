from pydantic import BaseModel, Field
from typing import Optional

class JobCreate(BaseModel):
    title: str
    description: str
    link: Optional[str] = None

class JobResponse(BaseModel):
    id: str
    title: str
    description: str
    link: Optional[str]
    company_id: str
    risk_score: float
    status: str
