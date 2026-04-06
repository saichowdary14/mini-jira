from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    project_id: int
    assigned_to: int

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


