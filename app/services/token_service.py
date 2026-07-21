from datetime import datetime,timedelta , timezone
from uuid import uuid4

from jose import JWTError
from fastapi import HTTPException , status
from sqlalchemy.orm import Session

from config.settings import settings
from app.core.security import encode_token , decode_token
from app.models.sessions import Session as UserSession
from app.schemas.jwt_token import Token_JWT
from app.schemas.token import AccessTokenLoad , RefreshTokenLoad
from app.models.user import User

class TokenService:

    def __init__(self,db:Session):
        self.db = db

    def _claims(self,*,user,token_type:str)->dict:
            claims = {
                "sub" : str(user.id),
                "type": token_type
            }

            if token_type == "access":
                claims["email"] = user.email
                claims["role"] = user.role
            return claims
    
    def create_access_token(self,user):
        return encode_token(data = self._claims(user=user , token_type="access"),
                            expires_delta = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                            token_type = "access")
    
    def create_refresh_token(self,user):
        return encode_token(data = self._claims(user=user, token_type="refresh"),
                            expires_delta = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
                            token_type = "refresh")
    
    def create_session(self , user , refresh_jti:str):
        session = UserSession(
            user_id = user.id,
            refresh_jti = refresh_jti,
            expires_at = datetime.now(timezone.utc) + timedelta(days= settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )

        self.db.add(session)

        return session
    
    def generate_token_pair(self,user):
       try:
            access_token , _ = self.create_access_token(user)
            refresh_token , refresh_jti = self.create_refresh_token(user)

            self.create_session(user=user , refresh_jti=refresh_jti)

            self.db.commit()
            return Token_JWT(
                access_token=access_token,
                refresh_token = refresh_token
            )
       except Exception:
           self.db.rollback()
           raise
    
    def verify_access_token(self, token:str):
        payload = decode_token(token,AccessTokenLoad)
        
        if payload.type != "access":
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "Invalid Token Type"
            )
        return AccessTokenLoad(
            sub = payload.sub,
            email = payload.email,
            role = payload.role,
            type = "Access",
            jti = payload.jti
        )
    
    def verify_refresh_token(self , token : str):
        payload =decode_token(token,RefreshTokenLoad)
        
        if payload.type != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )

        session = (
            self.db.query(UserSession)
            .filter(
                UserSession.refresh_jti == payload.jti
            )
            .first()
        )

        if not session:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session not found",
            )

        if session.revoked:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session revoked",
            )

        if session.expires_at < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Session expired",
            )

        return payload, session
    
    def rotate_refresh_token(self,refresh_token:str)->Token_JWT:

        payload , session = self.verify_refresh_token(refresh_token)

        session.revoked = True
        user_id = payload.sub
        user = self.db.get(User,user_id)

        if not user :
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail = "User not found"
            )
        
        try:
            new_access_token , _       = self.create_access_token(user)
            new_refresh_token , newjti = self.create_refresh_token(user)
            
            self.create_session(user = user , refresh_jti = newjti)

            self.db.commit()

            return Token_JWT(
                    access_token=new_access_token,
                    refresh_token=new_refresh_token,
            )
    
        except Exception:
            raise
      