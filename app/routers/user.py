from fastapi import FastAPI, APIRouter,Depends,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import user_create,user_response,login_request
from app.models.user  import User,Role,RolePermission,Permission
from app.core.security import hash_password,verify_password,create_access_token,get_current_user,require_permission
from ..database import get_db
from app.services.activity_service import log_activity
from app.services.user_services import promote_user_to_admin
from sqlalchemy.orm import Session
router=APIRouter(prefix="/users",tags=["Users"])


@router.post("/signup")
def user_signup(user:user_create,db:Session=Depends(get_db)):
    password_hash=hash_password(user.password)
    user_role = db.query(Role).filter(Role.name == "member").first()
    new_user=User(name=user.name,email=user.email,password=password_hash,role_id=user_role.id)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id":new_user.id,"name":new_user.name,"email":new_user.email,"role_id":user_role.id}

@router.post("/login")
def user_login(login_request:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==login_request.username).first()
    if not user:
        raise HTTPException(status_code=404,detail="user not found")
    if not verify_password(login_request.password,user.password):
        raise HTTPException(status_code=401,detail="Invalid password")
    access_token=create_access_token(data={"user_id":user.id})
    log_activity(db,user_id=user.id,message=f"{user.name} is succesfully loged in")
    db.commit()
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me",response_model=user_response)
def current_user(user=Depends(get_current_user),db:Session=Depends(get_db)):
    return user


@router.get("/all")
def get_users(db:Session=Depends(get_db)):
    users=db.query(User).all()
    return users



@router.put("/users/{user_id}/promote-admin")
def promote_user(user_id: int,db: Session = Depends(get_db),current_user = Depends(require_permission("project:create"))):
    return promote_user_to_admin(db, user_id, current_user)

# @router.get("/{user_id}",response_model=user_response)
# def get_user(user_id:int,db:Session=Depends(get_db)):
#     user=db.query(User).filter(User.id==user_id).first()
#     if not user:
#         raise HTTPException(status_code=404,detail="user not found")
#     return user



# @router.put("/{user_id}",response_model=user_response)
# def update_user(user_id:int,new_user:user_create,db:Session=Depends(get_db)):
#     user=db.query(User).filter(User.id==user_id).first()
#     if not user:
#         raise HTTPException(status_code=404,message="user not found")
#     user.name=new_user.name
#     user.email=new_user.email
#     db.commit()
#     db.refresh(user)
#     return user

# @router.delete("/{user_id}")
# def delete_user(user_id:int,db:Session=Depends(get_db)):
#     user=db.query(User).filter(User.id==user_id).first()
#     if not user:
#         raise HTTPException(status_code=404,detail="user not found")
#     db.delete(user)
#     db.commit()
#     return f"succesfully deleted user with id {user_id}"

@router.post("/projects")
def create_project(user=Depends(require_permission("project:create"))):
    return {"message": f"Project created by {user.name}"}

@router.post("/tasks/assign")
def assign_task(user=Depends(require_permission("task:assign"))):
    return {"message": f"Task assigned to {user.name}"}

@router.post("/tasks/view")
def assign_task(user=Depends(require_permission("task:view"))):
    return {"message": f"Task viewed by {user.name}"}

@router.post("/tasks/update")
def assign_task(user=Depends(require_permission("task:update"))):
    return {"message": f"Task updated by  {user.name}"}