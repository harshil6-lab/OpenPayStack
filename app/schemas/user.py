from pydantic import BaseModel , EmailStr , Field
from uuid import UUID
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
      message  :str
      user     : UserResponse