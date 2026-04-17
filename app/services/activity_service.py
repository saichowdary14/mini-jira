from app.models.activities import Activity

def log_activity(db,user_id, project_id,message ,task_id=None):
    activity=Activity(user_id=user_id,project_id=project_id,task_id=task_id,message=message)
    db.add(activity)
    return activity