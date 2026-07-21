from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from config.settings import settings
from uuid import uuid4
from jose import jwt, JWTError
from fastapi import HTTPException, status
from pydantic import BaseModel
from typing import Type


pwd_context = CryptContext( schemes = ["bcrypt"],deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password( plain_password : str,hashed_password : str)-> bool:
    return pwd_context.verify(plain_password, hashed_password)


#generic function to create tokens
def encode_token(data:dict,expires_delta: timedelta,token_type:str)-> tuple[str,str]:
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

def decode_token(token:str,schema : Type[BaseModel])->dict:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials"
    )

    try:
        payload = jwt.decode(token , settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        subject = payload.get("sub")
        
        if not subject:
            raise credentials_exception
        
        return schema.model_validate(payload)
    
    except JWTError:
        raise credentials_exception   
    
