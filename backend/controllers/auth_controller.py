from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, status

from sqlalchemy.orm import Session

from backend.db.base import get_db
from backend.model import Utente, Permesso, Paese
from typing import List, Dict

from backend.security.permissions import user_permissions
from backend.security.auth import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    get_current_user,
)

from backend.security.password import(
    verify_password
)

from backend.schemas.auth_controller_schemas import *


router = APIRouter(prefix="/auth", tags=["auth"])

def is_email(s: str) -> bool:
    return "@" in s and "." in s


# ----------- ENDPOINT LOGIN -----------

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
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

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenziali non valide",
        )

    # aggiorna last_login_at
    user.last_login_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    db.refresh(user)
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    return LoginResponse(user=user, access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh_token(payload: RefreshTokenRequest, db: Session = Depends(get_db)) -> RefreshTokenResponse:
    user_id = decode_refresh_token(payload.refresh_token)
    user = db.query(Utente).filter(Utente.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    if not user.attivo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Utente disattivato")
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))
    return RefreshTokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.get("/me/roles", response_model=UserRolesResponse)
def get_my_roles(user: Utente = Depends(get_current_user)) -> UserRolesResponse:
    # user.ruoli è già definito in Utente
    return UserRolesResponse(roles=user.ruoli)

@router.get("/countries", response_model=List[PaeseResponse])
@router.get("/coutries", response_model=List[PaeseResponse], include_in_schema=False)
def get_countries(db: Session = Depends(get_db)) -> List[PaeseResponse]:
    paesi = (
            db.query(
                Paese.id,
                Paese.nome,
                Paese.iso2,
                Paese.iso3,
                Paese.iso_numeric,
            )
            .filter(Paese.attivo == 1)
            .all()
        )
    return [
        PaeseResponse(
            id=r.id,
            nome=r.nome,
            iso2=r.iso2,
            iso3=r.iso3,
            iso_numeric=r.iso_numeric,
        )
        for r in paesi
    ]
    

@router.get("/me/permissions", response_model=UserPermissionResponse)
def get_my_permissions(user: Utente = Depends(get_current_user)) -> UserPermissionResponse:
    permissions_by_id: Dict[int, Permesso] = {}
    for ruolo in user.ruoli:
        for permesso in ruolo.permessi:
            permissions_by_id[permesso.id] = permesso
    return UserPermissionResponse(permissions=list(permissions_by_id.values()))

@router.get("/permissions_for_role", response_model=UserPermissionResponse)
def get_permissions_for_role(
    user: Utente = Depends(get_current_user),
    active_role_id: int | None = Header(default=None, alias="X-Active-Role-Id"),
) -> UserPermissionResponse:
    permissions = user_permissions(user, active_role_id=active_role_id)
    return UserPermissionResponse(permissions=permissions)
