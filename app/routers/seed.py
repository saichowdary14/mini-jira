from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.seed_services import seed_roles, seed_permissions,seed_role_permissions
from app.utils.constants import PERMISSIONS,ROLES

router = APIRouter(prefix="/seed", tags=["Seed"])


@router.post("/roles")
def seed_roles_route(db: Session = Depends(get_db)):
    created = seed_roles(db,ROLES)
    return {"created_roles": created}


@router.post("/permissions")
def seed_permissions_route(db: Session = Depends(get_db)):
    created = seed_permissions(db, PERMISSIONS)
    return {"created_permissions": created}

@router.post("/role-permissions")
def seed_role_permissions_route(db: Session = Depends(get_db)):
    created = seed_role_permissions(db)
    return {"created_mappings": created}