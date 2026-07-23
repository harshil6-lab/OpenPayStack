from sqlalchemy.orm import Session
from app.models.user import User
from app.models.wallet import Wallet
from app.models.sessions import Session as UserSession

from app.schemas.user import UserRegisterRequest , UserResponse , LoginResponse , LoginRequest
from app.schemas.device import DeviceInfo
from app.core.security import hash_password
from app.core.security import verify_password

from app.schemas.jwt_token import Token_JWT
from datetime import timedelta , timezone
from datetime import datetime
from app.services.token_service import TokenService
from uuid import UUID

from config.settings import settings

class UserService:
    
    def __init__(self,db:Session):
        self.db = db

    def register_user(self,payload: UserRegisterRequest):
            existing_user = (self.db.query(User).filter((User.email == payload.email)| (User.username == payload.username)).first())

            if existing_user :
                raise ValueError("credentials already exists")
            
            user = User(
                email = payload.email,
                username = payload.username,
                hashed_password=hash_password(payload.password)
            )

            self.db.add(user)
            self.db.flush()

            wallet = Wallet(user_id = user.id)
            self.db.add(wallet)
            self.db.commit()
            self.db.refresh(user)

            return user

    async def login_user(self,payload: LoginRequest,device : DeviceInfo):
            user = self.db.query(User).filter(User.email == payload.username).first()
            
            if not user: 
                raise ValueError("Invalid credentials")
            
            if not verify_password(payload.password,user.hashed_password):
                raise ValueError("Invalid credentials")
            
            token_service = TokenService(self.db)

            return token_service.generate_token_pair(user)

    async def logout(self,refresh_token: str):

         token_service = TokenService(self.db)

         _ , session = token_service.verify_refresh_token(refresh_token)

         session.revoked = True

         self.db.commit()

    async def logout_all_devices(self,user_id : UUID):
         self.db.query(UserSession).filter(
              UserSession.user_id == user_id,
              UserSession.revoked == False).update(
                   {"revoked" : True},
                   synchronize_session=False
              )

         self.db.commit()

    async def get_sessions(self,user_id : UUID):
           sessions = (
                self.db.query(UserSession)
                .filter(UserSession.user_id == user_id)
                .order_by(UserSession.last_used_at.desc())
                .all())
           return sessions
         