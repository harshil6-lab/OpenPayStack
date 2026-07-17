from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from config.settings import settings
from uuid import uuid4
from jose import jwt, JWTError
from app.schemas.token import Token as TokenPayload
from fastapi import HTTPException, status


pwd_context = CryptContext( schemes = ["bcrypt"],deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password( plain_password : str,hashed_password : str)-> bool:
    return pwd_context.verify(plain_password, hashed_password)


#generic function to create tokens
def create_token(data:dict,expires_delta: timedelta,token_type:str)-> tuple[str,str]:
    jti = str(uuid4())
    claims = data.copy()

    claims.update({
    "type": token_type,
    "jti": jti,
    "iat": datetime.now(timezone.utc),
    "exp": datetime.now(timezone.utc) + expires_delta,
    })

    token =  jwt.encode(claims, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token,jti

#access token generation and verification

def create_access_token(data : dict , expires_delta: timedelta)->str:
    
    return create_token(data=data , expires_delta = timedelta(minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES),token_type="access")

#veriy jwt token
def verify_access_token(token:str)->TokenPayload:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials"
    )

    try:
        payload = jwt.decode(token , settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        subject = payload.get("sub")
        
        if not subject:
            raise credentials_exception
        
        data = {
                "sub" : payload["sub"],
                "email" : payload.get("email"),
                "role" : payload.get("role"),
                 "jti" : payload.get("jti")
            }
        print(data)
        return TokenPayload(**data)
    
    except JWTError:
        raise credentials_exception   
    
def create_refresh_token(data: dict,expires_delta:timedelta):
    return create_token(data=data,expires_delta=timedelta(days = settings.REFRESH_TOKEN_EXPIRE_DAYS),token_type="refresh")
