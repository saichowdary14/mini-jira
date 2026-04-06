from sqlalchemy import Column,String,Integer,ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship

class Project(Base):
    __tablename__="projects"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    description=Column(String)
    created_by=Column(Integer,ForeignKey("users.id"))
    owner=relationship("User")