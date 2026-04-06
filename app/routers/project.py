from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.project import ProjectCreate,ProjectResponse
from app.services.project_service import create_project
from app.core.security import require_permission
router=APIRouter(prefix="/projects",tags=["projects"])

@router.post("/create", response_model=ProjectResponse)
def creating_project(project:ProjectCreate,db:Session=Depends(get_db),user=Depends(require_permission("project:create"))):
    return create_project(db,user,project)
