from fastapi import APIRouter, Depends, HTTPException
from database import db, to_obj
from schemas.company import CompanyCreate, CompanyResponse
from core.auth import get_current_user, require_roles
from bson import ObjectId

router = APIRouter()

@router.post("/register", response_model=CompanyResponse)
async def register_company(payload: CompanyCreate, user = Depends(get_current_user)):
    # only company-role users should register their company; or allow admins
    if user.get("role") not in ("company", "admin"):
        raise HTTPException(403, "Only company accounts can register a company")
    doc = payload.dict()
    doc.update({"is_verified": False, "trust_score": 0.0, "owner_id": str(user["_id"])})
    res = await db.companies.insert_one(doc)
    created = await db.companies.find_one({"_id": res.inserted_id})
    return CompanyResponse(**to_obj(created))

@router.post("/verify/{company_id}")
async def verify_company(company_id: str, admin = Depends(require_roles("admin"))):
    obj = await db.companies.find_one({"_id": ObjectId(company_id)})
    if not obj:
        raise HTTPException(404, "Company not found")
    await db.companies.update_one({"_id": ObjectId(company_id)}, {"$set": {"is_verified": True}})
    return {"ok": True}
