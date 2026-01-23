from __future__ import annotations


from fastapi import APIRouter, Depends, Header

from sqlalchemy.orm import Session

from backend.db.base import get_db
from backend.model import Utente
from typing import List

from backend.security.auth import get_current_user

from backend.schemas.auth_controller_schemas import *
from backend.services import auth_service
from backend.services import user_helpers


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    return auth_service.login(db,payload)

@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)) -> RefreshTokenResponse:
    return auth_service.refresh_token(db,payload)

@router.get("/me/roles", response_model=UserRolesResponse)
def get_my_roles(user: Utente = Depends(get_current_user)) -> UserRolesResponse:
    return auth_service.get_roles(user)

@router.get("/countries", response_model=List[PaeseResponse])
@router.get("/coutries", response_model=List[PaeseResponse], include_in_schema=False)
def get_countries(db: Session = Depends(get_db)) -> List[PaeseResponse]:
    return user_helpers.get_countries(db)
    
    
@router.get("/me/permissions", response_model=UserPermissionResponse)
def get_my_permissions(user: Utente = Depends(get_current_user)) -> UserPermissionResponse:
    return auth_service.get_permissions(user)

@router.get("/permissions_for_role", response_model=UserPermissionResponse)
def get_permissions_for_role(
    user: Utente = Depends(get_current_user),
    active_role_id: int | None = Header(default=None, alias="X-Active-Role-Id"),
) -> UserPermissionResponse:
    return auth_service.get_permissions_for_role(user, active_role_id)
