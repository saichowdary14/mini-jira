from app.models.task import Task
from fastapi import HTTPException
from app.services.activity_service import log_activity
from app.models.user import User

def create_task(task_create,db,user):
    user_id=user.id
    user_name=user.name
    assigned_to=task_create.assigned_to
    new_task=Task(title=task_create.title,
                  description=task_create.description,
                  created_by=user.id,
                  assigned_to=assigned_to if assigned_to else None,
                  priority=task_create.priority if task_create.priority else "medium",
                  project_id=task_create.project_id)
    db.add(new_task)
    db.flush()
    task_id=new_task.id
    if assigned_to:
        message = f"{user_name} created task and assigned to user {assigned_to}"
    else:
        message = f"{user_name} created task"
    log_activity(db,user_id=user_id,task_id=task_id,message=message)
    db.commit()
    db.refresh(new_task)
    return new_task
#_______________________________________________________________________________________________
#_______________________________________________________________________________________________

ALLOWED_TRANSITIONS = {
    "todo": ["in_progress"],
    "in_progress": ["done"],
    "done": []
}
def task_status_update( db,task_id,new_status:str,user):
    user_name=user.name
    user_id=user.id
    task=db.query(Task).filter(Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not(user.role.name=="admin" or task.created_by==user.id or task.assigned_to==user.id):
        raise HTTPException(status_code=403, detail="Not allowed to update this task")
    old_status=task.status.lower()
    if old_status == new_status.lower().strip():
        return {
            "task_id": task.id,
            "user_id": user_id,
            "message": f"Task already in '{new_status}' status"
        }
    new_status = new_status.lower().strip()
    if new_status not in ALLOWED_TRANSITIONS.get(old_status, []):
        raise HTTPException(status_code=400,detail=f"Invalid transition from {old_status} → {new_status}")
    task.status=new_status
    log_activity(db,user.id,f"{user.name} changed status from {old_status} → {new_status}",task.id)
    db.commit()
    db.refresh(task)
    return {"task_id":task.id,
            "user_id":user.id,
            "message":f"task {task_id} was updated by {user_name} as {new_status}"}
#_______________________________________________________________________________________________
#_______________________________________________________________________________________________


def assigning_task(db,task_id,assigned_to_id,user):
    user_id=user.id
    if user.role.name != "admin" and task.created_by != user.id:
        raise HTTPException(403, "Not allowed to assign task")
    task=db.query(Task).filter(Task.id==task_id).first()
    if not task:
        return None
    task.assigned_to=assigned_to_id
    log_activity(db,user.id,f"task {task_id} assigned to user {assigned_to_id} by person with id of {user_id}",task.id)
    db.commit()
    db.refresh(task)
    return {"task_id":task_id,
            "assigned_to":assigned_to_id,
            "message":f"task {task_id} assigned to user {assigned_to_id} by person with id of {user_id}"}