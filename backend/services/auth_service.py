from __future__ import annotations

from datetime import datetime, timezone
from typing import Dict

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.model import Permesso, Utente,Sessione
from backend.schemas.auth_controller_schemas import (
    LoginRequest,
    LoginResponse,
    UserPermissionResponse,
    UserRolesResponse,
)
from backend.schemas.UserManagement_controller_schemas import UpdateResponse

from backend.security.auth import create_session
from backend.security.password import verify_password
from backend.security.permissions import user_permissions
from backend.security.password import verify_password,hash_password

def setPassword(db:Session,username:str,old_psw:str,new_psw:str) -> UpdateResponse:
    user = db.query(Utente).filter(Utente.username == username).one_or_none()
    if (user == None): return UpdateResponse(Result=-1,update_timestamp=datetime.now())
    if(not verify_password(old_psw,user.password_hash)): return UpdateResponse(Result=-1,update_timestamp=datetime.now())
    user.password_hash = hash_password(new_psw)
    db.commit()
    db.refresh(user)
    return UpdateResponse(Result=1,update_timestamp=user.updated_at)

def is_email(value: str) -> bool:
    return "@" in value and "." in value

def login(db: Session, payload: LoginRequest) -> LoginResponse:
    identifier = payload.identifier.strip()

    q = db.query(Utente)
    if is_email(identifier):
        user = q.filter(Utente.email == identifier).first()
    else:
        user = q.filter(Utente.username == identifier).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenziali non valide",
        )

    if not user.attivo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utente disattivato",
        )
    
    if  verify_password("RESET_REQUIRED",user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
            detail="PASSWORD_RESET_REQUIRED",
        )

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenziali non valide",
        )

    user.last_login_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    db.refresh(user)
    session = create_session(db, user)
    return LoginResponse(user=user, session_token=session.token, expires_at=session.expires_at)


def get_roles(user: Utente) -> UserRolesResponse:
    return UserRolesResponse(roles=user.ruoli)


def get_permissions(user: Utente) -> UserPermissionResponse:
    permissions_by_id: Dict[int, Permesso] = {}
    for ruolo in user.ruoli:
        for permesso in ruolo.permessi:
            permissions_by_id[permesso.id] = permesso
    return UserPermissionResponse(permissions=list(permissions_by_id.values()))


def get_permissions_for_role(user: Utente, active_role_id: int | None) -> UserPermissionResponse:
    permissions = user_permissions(user, active_role_id=active_role_id)
    return UserPermissionResponse(permissions=permissions)