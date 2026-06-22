from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.schemas.user import UserRegisterRequest,UserResponse
from app.services.user_service import register_user

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model = UserResponse)
def register(payload: UserRegisterRequest,db:Session = Depends(get_db)):
    try : 
        user = register_user(db = db , payload = payload )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))