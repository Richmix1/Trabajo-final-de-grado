from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.core.security import create_access_token, hash_password, verify_password
from app.db.mongo import get_database
from app.models.schemas import Token, UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate) -> Token:
    db = get_database()
    existing = await db.users.find_one({"email": payload.email})
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user_id = str(uuid4())
    user_doc = {
        "_id": user_id,
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
        "created_at": datetime.utcnow(),
    }
    await db.users.insert_one(user_doc)

    access_token = create_access_token({"sub": user_id})
    return Token(access_token=access_token)


@router.post("/login", response_model=Token)
async def login(payload: UserLogin) -> Token:
    db = get_database()
    user = await db.users.find_one({"email": payload.email})
    if not user or not verify_password(payload.password, user.get("hashed_password", "")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token({"sub": user["_id"]})
    return Token(access_token=access_token)
