from app.core.database import SessionLocal
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verify_access_token
from fastapi import HTTPException, status
from app.models.user import User

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
async def get_current_user(token: str = Depends(oauth2_scheme), db=Depends(get_db)):
    
    
    token = verify_access_token(token)

    user = db.query(User).filter(User.id == token.sub).first()

    if not user :
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )
    
    return user
