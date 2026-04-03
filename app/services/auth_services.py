
from app.models.user import Role,Permission,RolePermission

def get_permissions_by_role(role_id,db):
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        return []
    return [rp.permission.name for rp in role.role_permissions]