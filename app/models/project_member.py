from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Enum
from ..database import Base
import enum

class ProjectRole(enum.Enum):
    admin = "admin"
    team_lead = "team_lead"
    member = "member"



class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    role = Column(Enum(ProjectRole), default=ProjectRole.member, nullable=False)
    
    user = relationship("User", back_populates="project_members")
    project = relationship("Project", back_populates="members")