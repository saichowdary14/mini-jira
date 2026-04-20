from pydantic import BaseModel
from typing import Optional

class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_to: Optional[int] = None
    priority: Optional[str] = "medium"

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    priority: str

    class Config:
        from_attributes = True

class TaskUpdateStatus(BaseModel):
    status:str
    
class TaskUdateResponse(BaseModel):
    task_id:int
    user_id:int
    message:str

    class Config:
        from_attributes = True

class Taskassign_Request(BaseModel):
    user_id:int

class Taskassign_Response(BaseModel):
    task_id:int
    assigned_to:int
    message:str


