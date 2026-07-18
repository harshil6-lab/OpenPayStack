from sqlalchemy.orm import Session
from app.models.user import User
from app.models.wallet import Wallet
from app.models.sessions import Session as UserSession

from app.schemas.user import UserRegisterRequest , UserResponse , LoginResponse , LoginRequest
from app.core.security import hash_password
from app.core.security import verify_password

from app.schemas.jwt_token import Token_JWT
from datetime import timedelta , timezone
from datetime import datetime
from app.services.token_service import TokenService


from config.settings import settings
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
    
    token_service = TokenService(db)

    return token_service.generate_token_pair(user)