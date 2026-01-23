from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from backend.db.base import get_db
from backend.model import Utente
from backend.security.dependencies import require_permission,get_current_user

from backend.schemas.UserManagement_controller_schemas import *
from backend.services import user_service


router = APIRouter(prefix="/userManagement", tags=["userManagement"])

@router.get("/roles",response_model=List[RolesResponse])
def getAllRoles(
    db: Session = Depends(get_db),
    _: Utente = Depends(get_current_user)
) -> List[RolesResponse]:
    return user_service.list_roles(db)

@router.post("/addUser", response_model=CreatedUserResponse)
def add_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: Utente = Depends(require_permission("user.create")),
) -> CreatedUserResponse:
    return user_service.create_user(db,payload)


@router.patch("/user/pswChange",response_model=UpdateResponse)
def modifyUser(
    payload: PasswordChange,
    db: Session = Depends(get_db),
)-> UpdateResponse:
    pass


@router.patch("/me/pswChange",response_model=UpdateResponse)
def modifyUser(
    payload: PasswordChange,
    db: Session = Depends(get_db),
    user: Utente = Depends(get_current_user)
)-> UpdateResponse:
    return user_service.update_password(
        db,
        user,
        old_password=payload.old_password,
        new_password=payload.new_password,
        )


@router.patch("/user/modify",response_model=UpdateResponse)
def modifyUser(
    payload: TutorSettingsUpdateRequest,
    db: Session = Depends(get_db),
    _: Utente = Depends(require_permission("user.user_update"))
)-> UpdateResponse:
    pass

@router.patch("/me/modify",response_model=UpdateResponse)
def modifyMe(
    payload: TutorSettingsUpdateRequest,
    db: Session = Depends(get_db),
    user: Utente = Depends(get_current_user)
)-> UpdateResponse:
    return user_service.update_profile(
        db,
        user,
        payload
    )