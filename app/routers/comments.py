from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.comment import CommentCreate, CommentResponse
from app.services.comment_service import create_comment
from app.core.security import require_permission
from app.models.comment import Comment

router = APIRouter(prefix="/comments", tags=["Comments"])

@router.post("/", response_model=CommentResponse)
def add_comment(data: CommentCreate,db: Session = Depends(get_db),user=Depends(require_permission("comment:create"))):
    return create_comment(db, user, data)


@router.get("/task/{task_id}", response_model=list[CommentResponse])
def get_comments(task_id: int,db: Session = Depends(get_db),user=Depends(require_permission("task:view"))):
    return db.query(Comment).filter(Comment.task_id == task_id).all()