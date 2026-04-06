from app.models.project import Project
def create_project(db,user,project):
    project=Project(name=project.name,description=project.description,created_by=user.id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project