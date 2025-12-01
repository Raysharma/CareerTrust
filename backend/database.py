# backend/database.py
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

load_dotenv()  # loads .env

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise RuntimeError("MONGO_URI not set in .env")

client = AsyncIOMotorClient(MONGO_URI)
db = client.get_database("careertrust")  # database name

def to_obj(obj):
    if not obj:
        return obj
    o = dict(obj)
    if "_id" in o:
        o["id"] = str(o["_id"])
        del o["_id"]
    return o
