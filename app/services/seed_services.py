from app.models.user import Role, Permission,RolePermission


def seed_roles(db,roles):
    created = []
    for role_name in roles:
        existing = db.query(Role).filter(Role.name == role_name).first()
        if not existing:
            db.add(Role(name=role_name))
            created.append(role_name)

    db.commit()
    return created


def seed_permissions(db, permissions_list):
    created = []
    for perm in permissions_list:
        existing = db.query(Permission).filter(Permission.name == perm).first()
        if not existing:
            db.add(Permission(name=perm))
            created.append(perm)
    db.commit()
    return created



def seed_role_permissions(db):
    role_map = {
        "admin": "ALL",
        "team_lead": [
            "project:create", "project:view", "project:update",
            "task:create", "task:view", "task:update", "task:assign",
            "comment:create", "user:invite"
        ],
        "member": [
            "task:view", "task:update", "comment:create"
        ]
    }

    created = []

    for role_name, perms in role_map.items():
        role = db.query(Role).filter(Role.name == role_name).first()
        if not role:
            continue

        # Admin gets all permissions
        if perms == "ALL":
            permissions = db.query(Permission).all()
        else:
            permissions = db.query(Permission).filter(Permission.name.in_(perms)).all()
        for perm in permissions:
            exists = db.query(RolePermission).filter(RolePermission.role_id == role.id,RolePermission.Permission_id == perm.id).first()
            if not exists:
                rp = RolePermission(role_id=role.id,Permission_id=perm.id)
                db.add(rp)
                created.append(f"{role.name} → {perm.name}")

    db.commit()
    return created