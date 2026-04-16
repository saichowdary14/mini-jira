import os
from passlib.context import CryptContext
import os

pwdcontext=CryptContext(schemes=["bcrypt"],deprecated="auto")
def hash_password(password:str):
    return pwdcontext.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwdcontext.verify(plain_password, hashed_password)

#_________________________________________________________________________
#_________________________________________________________________________

from jose import JWTError,jwt
from datetime import datetime , timedelta , timezone

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
def create_access_token(data:dict):
    to_encode=data.copy()
    exp_time=datetime.now(timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":exp_time})
    encoded_jwt=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
    
def verify_access_token(token:str):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        user_id=payload.get("user_id")
        return user_id
    except JWTError:
        return None
    
#_______________________________________________________________________________________
#_______________________________________________________________________________________

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme=OAuth2PasswordBearer(tokenUrl="users/login")

def get_current_user(access_token:str=Depends(oauth2_scheme),db:Session=Depends(get_db)):
    user_id=verify_access_token(access_token)
    if not user_id:
        raise HTTPException(status_code=401,detail="invalid token ")
    user=db.query(User).filter(User.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user
#_______________________________________________________________________________________________
#_______________________________________________________________________________________________



from app.services.auth_services import get_permissions_by_role

def require_permission(permission_name:str):
    def checker(user=Depends(get_current_user),db:Session=Depends(get_db)):
        permissions=get_permissions_by_role(user.role_id,db)
        if permission_name not in permissions:
            raise HTTPException(status_code=403,detail="You do not have permission")
        return user
    return checker