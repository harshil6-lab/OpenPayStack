from pydantic import BaseModel, EmailStr

class Token_JWT(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str = "bearer"
    email : str
    role : str