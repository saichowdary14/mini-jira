from sqlalchemy import Column,String,Integer,ForeignKey
from ..database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String)
    email=Column(String, unique=True,index=True)
    password=Column(String,nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role=relationship("Role",back_populates="users")

class Role(Base):
    __tablename__="roles"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,unique=True,nullable=False)
    users=relationship("User",back_populates="role")
    role_permissions=relationship("RolePermission",back_populates="role")

class Permission(Base):
    __tablename__="permissions"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,unique=True,nullable=False)
    role_permissions=relationship("RolePermission",back_populates="permission")


class RolePermission(Base):
    __tablename__="role_permissions"
    id=Column(Integer,primary_key=True,index=True)
    role_id=Column(Integer,ForeignKey("roles.id",ondelete="CASCADE"))
    Permission_id=Column(Integer,ForeignKey("permissions.id",ondelete="CASCADE"))
    role=relationship("Role",back_populates="role_permissions")
    permission=relationship("Permission",back_populates="role_permissions")
