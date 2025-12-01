from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.users import router as user_router
from routes.verify import router as verify_router

app = FastAPI(title="CareerTrust- Scam Verification API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"status": "CareerTrust backend running"}

app.include_router(user_router, prefix="/users", tags=["Users"])
app.include_router(verify_router, prefix="/verify", tags=["Verification"])