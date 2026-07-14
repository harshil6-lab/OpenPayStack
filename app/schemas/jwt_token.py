from pydantic import BaseModel, EmailStr

class Token_JWT(BaseModel):
    access_token : str
    token_type : str = "bearer"