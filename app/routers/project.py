from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.project import ProjectCreate,ProjectResponse,AddUserToProject
from app.services.project_service import create_project,add_user_to_project
from app.core.security import require_permission
router=APIRouter(prefix="/projects",tags=["projects"])

@router.post("/create", response_model=ProjectResponse)
def creating_project(project:ProjectCreate,db:Session=Depends(get_db),user=Depends(require_permission("project:create"))):
    return create_project(db,user,project)

@router.post("/projects/{project_id}/add-user")
def add_user(project_id: int,request: AddUserToProject,db: Session = Depends(get_db),current_user=Depends(require_permission("user:invite"))):
    return add_user_to_project(db=db,
                               project_id=project_id,
                               user_id=request.user_id,
                               role=request.role,
                               current_user=current_user)