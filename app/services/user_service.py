from sqlalchemy.orm import Session
from app.models.user import User
from app.models.wallet import Wallet

from app.schemas.user import UserRegisterRequest , UserResponse , LoginResponse , LoginRequest
from app.core.security import hash_password
from app.core.security import verify_password

from app.core.security import create_access_token
from app.schemas.jwt_token import Token_JWT
from datetime import timedelta

def register_user(db:Session,payload: UserRegisterRequest):
    existing_user = (db.query(User).filter((User.email == payload.email)| (User.username == payload.username)).first())

    if existing_user :
        raise ValueError("credentials already exists")
    
    user = User(
        email = payload.email,
        username = payload.username,
        hashed_password=hash_password(payload.password)
    )

    db.add(user)
    db.flush()

    wallet = Wallet(user_id = user.id)
    db.add(wallet)
    db.commit()
    db.refresh(user)

    return user

def login_user(db:Session,payload: LoginRequest):
    user = db.query(User).filter(User.email == payload.username).first()
    
    if not user: 
        raise ValueError("Invalid credentials")
    
    if not verify_password(payload.password,user.hashed_password):
        raise ValueError("Invalid credentials")
    
    claim = {
        "sub" : str(user.id),
        "email" : user.email,
        "role" : user.role
    }

    create_token = create_access_token(claim,expires_delta=timedelta(minutes=15))

    return Token_JWT(access_token=create_token,token_type="bearer")