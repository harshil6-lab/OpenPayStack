from sqlalchemy.orm import Session
from app.models.user import User
from app.models.wallet import Wallet
from app.models.sessions import Session as UserSession

from app.schemas.user import UserRegisterRequest , UserResponse , LoginResponse , LoginRequest
from app.core.security import hash_password
from app.core.security import verify_password

from app.core.security import create_access_token , create_refresh_token
from app.schemas.jwt_token import Token_JWT
from datetime import timedelta , timezone
from datetime import datetime


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
    
    claim = {
        "sub" : str(user.id),
        "email" : user.email,
        "role" : user.role
    }

    access_token,_ = create_access_token({
        "sub" : str(user.id),
        "email" : user.email,
        "role" : user.role
    },expires_delta=timedelta(minutes=15))

    refresh_token,refresh_jti = create_refresh_token({
        "sub" : str(user.id)
    },expires_delta=timedelta(days = 30))

    session = UserSession(user_id = user.id , refresh_jti = refresh_jti ,expires_at = datetime.now(timezone.utc)+timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
    db.add(session)
    db.commit()
    db.refresh(session)
    return Token_JWT(access_token=access_token,refresh_token=refresh_token,token_type="bearer")