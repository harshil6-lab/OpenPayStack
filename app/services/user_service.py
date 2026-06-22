from sqlalchemy.orm import Session
from app.models.user import User
from app.models.wallet import Wallet

from app.schemas.user import UserRegisterRequest
from app.core.security import hash_password

def register_user(db:Session,payload: UserRegisterRequest):
    existing_user = (db.query(User).filter((User.email == payload.email)| (User.username == payload.username)).first())

    if existing_user :
        raise ValueError("user already exists")
    
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