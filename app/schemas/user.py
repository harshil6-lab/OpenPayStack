from pydantic import BaseModel , EmailStr , Field
from uuid import UUID
from datetime import datetime

class UserRegisterRequest(BaseModel):
    email : EmailStr
    username : str = Field(
        min_length = 3,
        max_length = 50
    )
    password : str = Field(min_length = 8 , max_length = 128)


class UserResponse(BaseModel):
    id : UUID
    email : str
    username : str
    is_verified : bool

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
     email : EmailStr
     password  : str = Field(min_length = 8 , max_length = 128)

class LoginResponse(BaseModel):
      access_token : str
      token_type : str = "bearer"

class CurrentUserResponse(BaseModel):
    id : UUID
    email : str
    username : str
    is_verified : bool
    role : str
    created_at : datetime

    class Config:
        from_attributes = True