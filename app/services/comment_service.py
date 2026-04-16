from app.models.comment import Comment
from app.services.activity_service import log_activity


def create_comment(db,user,data):
    message=data.content
    task_id=data.task_id
    user_id=user.id
    comment=Comment(content=message,task_id=task_id,user_id=user_id)
    db.add(comment)
    log_activity(db,user_id=user_id,task_id=task_id,message=message)
    db.commit()
    db.refresh(comment)
    return comment