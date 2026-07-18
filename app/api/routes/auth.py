from fastapi import APIRouter , Depends , HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

from app.schemas.user import UserRegisterRequest,UserResponse,LoginResponse,LoginRequest
from app.api.dependencies import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from app.services.user_service import UserService

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model = UserResponse)
def register(payload: UserRegisterRequest,db:Session = Depends(get_db)):
    
    register_service = UserService(db)

    try : 
        return register_service.register_user(payload)    
    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))

@router.post("/login",response_model = LoginResponse)
def login(form_data:OAuth2PasswordRequestForm=Depends(),db:Session = Depends(get_db)):
    payload = LoginRequest(
        username = form_data.username,
        password = form_data.password
    )
    service = UserService(db)
    try : 
        return service.login_user(payload)

    except ValueError as e:
        raise HTTPException(status_code=401,detail=str(e))

