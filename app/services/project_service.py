from app.models.project import Project
from app.models.project_member import ProjectMember
from app.services.activity_service import log_activity
from app.models.user import User
from fastapi import HTTPException
def create_project(db,user,project):
    user_name=user.name
    project_name=project.name
    description=project.description
    user_id=user.id
    project=Project(name=project.name,description=project.description,created_by=user.id)
    db.add(project)
    log_activity(db,user_id=user_id,message=f"{user_name} is created a new project with name of {project_name}")
    db.commit()
    db.refresh(project)
    member = ProjectMember(user_id=user.id,project_id=project.id,role=user.role.name)
    db.add(member)
    db.commit()
    return project


#________________________________________________________________________________________________
#________________________________________________________________________________________________


ALLOWED_INVITE_ROLES = ["admin", "team_lead"]
def add_user_to_project(db,project_id,user_id,role,current_user):
     # Check if target user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    #check if user is already a member of the project
    existing_member=db.query(ProjectMember).filter(ProjectMember.project_id==project_id,ProjectMember.user_id==user_id).first()
    if existing_member:
        raise HTTPException(status_code=400, detail="User is already a member of the project")
    # Check if current user is project admin
    current_member=db.query(ProjectMember).filter(ProjectMember.project_id == project_id,ProjectMember.user_id == current_user.id).first()
    if not current_member or current_member.role not in ALLOWED_INVITE_ROLES:
        raise HTTPException(status_code=403, detail="Not allowed to invite users")
    new_member = ProjectMember(user_id=user_id,project_id=project_id,role=role)
    try:
        db.add(new_member)
        db.flush()  # get ID if needed
        log_activity(db,user_id=current_user.id,project_id=project_id,message=f"{current_user.name} added user {user.name} to project with role {role}")
        db.commit()
        db.refresh(new_member)
    except Exception as e:
        db.rollback()
        print("ERROR:", str(e))   # 👈 VERY IMPORTANT
        raise HTTPException(status_code=500, detail=str(e))
    return {
        "message": f"User {user_id} added to project {project_id} as {role}"}



SYSTEM_ADMIN_ROLE_ID = 1


def update_member_role(db, project_id, request, current_user):
    # 1. Check project exists
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    # 2. Permission check
    if current_user.role_id != SYSTEM_ADMIN_ROLE_ID:
        current_member = db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id,
            ProjectMember.user_id == current_user.id).first()
        if not current_member:
            raise HTTPException(status_code=403,detail="You are not part of this project")
        if current_member.role != "admin":
            raise HTTPException(status_code=403,detail="Only project admin can change roles")
    # 3. Get target member
    member = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.user_id == request.user_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")
    # 4. Already same role check (🔥 your requirement)
    if member.role == request.new_role:
        raise HTTPException(status_code=400,detail=f"User is already {member.role}")

    # 5. Validate role
    VALID_ROLES = ["admin", "member", "team_lead"]

    if request.new_role not in VALID_ROLES:
        raise HTTPException(status_code=400, detail="Invalid role")

    # 6. Prevent removing last admin
    if member.role == "admin" and request.new_role != "admin":
        admins_count = db.query(ProjectMember).filter(
            ProjectMember.project_id == project_id,
            ProjectMember.role == "admin"
        ).count()

        if admins_count == 1:
            raise HTTPException(status_code=400,detail="Cannot remove last admin")

    # 7. Update role
    old_role = member.role
    member.role = request.new_role

    db.commit()
    db.refresh(member)

    # 8. Log activity
    log_activity(db,current_user.id,project_id,f"{current_user.name} changed role of user {member.user_id} from {old_role} → {request.new_role}")

    return {
        "message": "Role updated successfully",
        "user_id": member.user_id,
        "new_role": member.role
    }