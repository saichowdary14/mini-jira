
from app.models.user import Role,Permission,RolePermission

def get_permissions_by_role(role_name,db):
    role = db.query(Role).filter(Role.name == role_name).first()
    if not role:
        return []
    return [rp.permission.name for rp in role.role_permissions]


