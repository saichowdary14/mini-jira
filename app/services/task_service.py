from app.models.task import Task
from fastapi import HTTPException

def create_task(task_create,db,user):
    new_task=Task(title=task_create.title,
                  description=task_create.description,
                  created_by=user.id,
                  assigned_to=task_create.assigned_to,
                  project_id=task_create.project_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task





def task_status_update( db,task_id,status:str,user):
    task=db.query(Task).filter(Task.id==task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not(user.role.name=="admin" or task.created_by==user.id or task.assigned_to==user.id):
        raise HTTPException(status_code=403, detail="Not allowed to update this task")
    task.status=status
    db.commit()
    db.refresh(task)
    return {"task_id":task.id,
            "user_id":user.id,
            "message":f"task {task_id} was updated by {user.id} as {status}"}

def assigning_task(task_id,db,assigned_to_id):
    task=db.query(Task).filter(Task.id==task_id).first()
    if not task:
        return None
    task.assigned_to=assigned_to_id
    db.commit()
    db.refresh(task)
    return task