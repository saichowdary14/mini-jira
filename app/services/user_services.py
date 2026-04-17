from fastapi import HTTPException
from app.models.user import User,Role
from app.services.activity_service import log_activity


def promote_user_to_admin(db, user_id, current_user):

    #  Only admin can promote
    if current_user.role.name != "admin":
        raise HTTPException(403, "Not allowed")

    # Check user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    # Get admin role
    admin_role = db.query(Role).filter(Role.name == "admin").first()
    if not admin_role:
        raise HTTPException(404, "Admin role not found")

    # Already admin check
    if user.role_id == admin_role.id:
        return {"message": "User is already admin"}

    # Update role
    user.role_id = admin_role.id
    log_activity(db=db,user_id=current_user.id,message=f"{current_user.name} promoted user {user.name} to admin")
    db.commit()
    db.refresh(user)

    return {
        "message": f"User {user.name} promoted to admin"
    }