from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.schemas.user import UserRegisterRequest,UserResponse,LoginResponse,LoginRequest
from app.services.user_service import register_user ,login_user
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model = UserResponse)
def register(payload: UserRegisterRequest,db:Session = Depends(get_db)):
    try : 
        user = register_user(db = db , payload = payload )
        return user
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.post("/login",response_model = LoginResponse)
def login(payload:LoginRequest,db:Session = Depends(get_db)):
    try : 
        user = login_user(db = db , payload = payload )
        return user
    except ValueError as e:
        raise HTTPException(status_code=401,detail=str(e))

@router.get("/me",response_model = UserResponse)
def get_current_user(current_user: UserResponse = Depends(get_current_user)):
    return current_user