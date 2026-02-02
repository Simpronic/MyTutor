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
    _: Utente = Depends(require_permission("USER_CREATE")),
) -> CreatedUserResponse:
    return user_service.create_user(db,payload)

@router.patch("/user/toggleUser",response_model=UpdateResponse)
def toggleUser(
    id: int,
    db: Session = Depends(get_db),
    _: Utente = Depends(require_permission("USER_UPDATE"))
) -> UpdateResponse:
    return user_service.toggleUser(db,id)

@router.get("/user/userInfos", response_model=UserFullResponse)
def getUserInfos(
    user_id: int,
    db: Session = Depends(get_db),
    _:Utente = Depends(require_permission("USER_READ"))
):
    return user_service.getUserInfos(db,user_id)

@router.get("/allUsers",response_model=List[UserFullResponse])
def getAllUsers(
    db: Session = Depends(get_db),
    u: Utente = Depends(require_permission("USER_READ"))
) -> List[UserFullResponse]:
    return user_service.getAllUsers(u,db)

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

@router.get("/me", response_model=UserFullResponse)
def get_me(
    user: Utente = Depends(get_current_user),
) -> UserFullResponse:
    return user

@router.patch("/user/modify",response_model=UpdateResponse)
def modifyUser(
    payload: TutorSettingsUpdateRequest,
    db: Session = Depends(get_db),
    _: Utente = Depends(require_permission("USER_UPDATE"))
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