from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.activities import Activity
from app.schemas.activity import ActivityResponse
from app.core.security import require_permission

router = APIRouter(prefix="/activities", tags=["Activities"])

@router.get("/task/{task_id}", response_model=list[ActivityResponse])
def get_activities(task_id: int,db: Session = Depends(get_db),user=Depends(require_permission("task:view"))):
    return db.query(Activity).filter(Activity.task_id == task_id).all()