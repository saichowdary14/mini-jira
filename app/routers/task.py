from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.task import TaskCreate, TaskResponse,TaskUpdateStatus,TaskUdateResponse,Taskassign_Request,Taskassign_Response
from app.services.task_service import create_task,task_status_update,assigning_task
from app.core.security import require_permission


router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/create",response_model=TaskResponse)
def creating_task(task_create:TaskCreate,db:Session=Depends(get_db), user=Depends(require_permission("task:create"))):
    return create_task(task_create,db,user)

@router.post("/{task_id}/status",response_model=TaskUdateResponse)
def updating_task_status(task_id,status_request:TaskUpdateStatus,db:Session=Depends(get_db),user=Depends(require_permission("task:update"))):
    return task_status_update(db,task_id,status_request.status,user)

@router.post("/{task_id}/assign",response_model=Taskassign_Response)
def task_assign(task_id,assign_request:Taskassign_Request,db:Session=Depends(get_db),user=Depends(require_permission("task:assign"))):
    return assigning_task(db,task_id,assign_request.user_id,user)
