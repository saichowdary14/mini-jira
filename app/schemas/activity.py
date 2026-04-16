from pydantic import BaseModel
from datetime import datetime

class ActivityResponse(BaseModel):
    id: int
    message: str
    task_id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True