from fastapi import APIRouter, Depends, HTTPException
from database import db, to_obj
from schemas.job import JobCreate, JobResponse
from core.auth import require_roles, get_current_user
from core.risk import heuristic_risk
from bson import ObjectId

router = APIRouter()

@router.post("/create", response_model=JobResponse)
async def create_job(payload: JobCreate, user = Depends(get_current_user)):
    # user must be a company and their company must be verified - simplified: owner_id check
    # find company for this user (for MVP, we assume one company per user)
    comp = await db.companies.find_one({"owner_id": str(user["_id"])})
    if not comp:
        raise HTTPException(403, "Company not registered")
    if not comp.get("is_verified"):
        raise HTTPException(403, "Company not verified")
    # risk check
    res = heuristic_risk(payload.description, comp.get("email"))
    doc = payload.dict()
    doc.update({"company_id": str(comp["_id"]), "risk_score": res["score"], "status": res["status"], "analysis": res["reasons"]})
    r = await db.jobs.insert_one(doc)
    j = await db.jobs.find_one({"_id": r.inserted_id})
    return JobResponse(**to_obj(j))
