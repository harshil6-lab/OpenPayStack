from pydantic import BaseModel, EmailStr

class AccessTokenLoad(BaseModel):
    sub   :   str
    email : EmailStr
    role  : str
    type  : str
    jti   : str

class RefreshTokenLoad(BaseModel):
    sub  : str
    type : str
    jti  : str