from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from config.settings import settings
import uuid
from jose import jwt, JWTError
from app.schemas.token import Token as TokenPayload
from fastapi import HTTPException, status


pwd_context = CryptContext( schemes = ["bcrypt"],deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password( plain_password : str,hashed_password : str)-> bool:
    return pwd_context.verify(plain_password, hashed_password)

#access token generation and verification

def create_access_token(data : dict , expires_delta: timedelta)->str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))

    to_encode.update(
        {
            "exp" : expire,
            "iat" : datetime.now(timezone.utc),
            "jid" : str(uuid.uuid4())
        }
    )


    encoded_jwt = jwt.encode(to_encode , settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt

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
        
        return TokenPayload({
            "sub" : payload["sub"],
            "email" : payload.get("email"),
            "role" : payload.get("role"),
            "jti" : payload.get("jti")
        })
    
    except JWTError:
        raise credentials_exception   
