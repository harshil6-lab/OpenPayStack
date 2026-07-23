from app.core.database import SessionLocal
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status
from app.models.user import User
from app.services.token_service import TokenService

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    
    token_service = TokenService(db)
    payload = token_service.verify_access_token(token)
    user = db.query(User).filter(User.id == payload.sub).first()

    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    return user
