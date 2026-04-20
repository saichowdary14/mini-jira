from pydantic import BaseModel
from typing import Optional

class ProjectCreate(BaseModel):
    name: str
    description: str

class ProjectResponse(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True

class AddUserToProject(BaseModel):
    user_id: int
    role: Optional[str] = "member"

class UpdateRoleRequest(BaseModel):
    user_id: int
    new_role: str