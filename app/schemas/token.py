from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    sub : str
    email : EmailStr
    role  :str
    jti   :str