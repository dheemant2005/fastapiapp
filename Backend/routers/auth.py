from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.users import User
from schemas.users import UserCreate, UserResponse, Login_User
from schemas.token import Token
from database import get_db
from utils.security import hash_password, verify_password
from utils.token import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login_user(user: Login_User, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(user.password, existing_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    access_token = create_access_token(data={"sub":str(existing_user.id),"role":existing_user.role})
    return {"token":access_token, "token_type":"Bearer"}