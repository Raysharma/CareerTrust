# backend/routes/users.py
from fastapi import APIRouter, HTTPException, Depends
from database import db, to_obj
from schemas.user import UserCreate, UserResponse, LoginRequest, TokenResponse
from core.auth import get_password_hash, verify_password, create_access_token, get_current_user
from bson import ObjectId

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(user: UserCreate):
    email = user.email.lower().strip()
    if await db.users.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already registered")
    doc = {
        "name": user.name.strip(),
        "email": email,
        "password": get_password_hash(user.password),
        "role": user.role
    }
    result = await db.users.insert_one(doc)
    created = await db.users.find_one({"_id": result.inserted_id})
    created.pop("password", None)
    return UserResponse(**to_obj(created))

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    email = payload.email.lower().strip()
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(payload.password, user.get("password","")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": str(user["_id"]), "role": user.get("role")})
    return TokenResponse(access_token=token)

@router.get("/me", response_model=UserResponse)
async def me(current = Depends(get_current_user)):
    current.pop("password", None)
    return UserResponse(**to_obj(current))
