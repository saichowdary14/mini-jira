from app.models.project import Project
from app.models.project_member import ProjectMember,ProjectRole
from app.services.activity_service import log_activity
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
    member = ProjectMember(
        user_id=user.id,
        project_id=project.id,
        role=ProjectRole.admin)

    db.add(member)
    db.commit()

    return project