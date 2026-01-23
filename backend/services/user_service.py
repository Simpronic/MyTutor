from __future__ import annotations

import secrets
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.model import Ruolo, Utente, UtenteRuolo
from backend.schemas.UserManagement_controller_schemas import (
    CreatedUserResponse,
    RolesResponse,
    TutorSettingsUpdateRequest,
    UpdateResponse,
    UserCreate,
)
from backend.security.password import hash_password, pwd_hasher, verify_password
from backend.services.user_helpers import ensure_unique_user_fields


def list_roles(db: Session) -> List[RolesResponse]:
    return db.query(Ruolo).all()


def create_user(db: Session, payload: UserCreate) -> CreatedUserResponse:
    ensure_unique_user_fields(
        db,
        username=payload.username,
        email=payload.email,
        cf=payload.cf,
    )

    role_names = [role.nome for role in payload.ruoli]
    roles = []
    if role_names:
        roles = db.query(Ruolo).filter(Ruolo.nome.in_(role_names)).all()
        if len(roles) != len(set(role_names)):
            missing = sorted(set(role_names) - {role.nome for role in roles})
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ruoli non trovati: {', '.join(missing)}",
            )

    raw_password = secrets.token_urlsafe(12)
    user = Utente(
        username=payload.username,
        email=payload.email,
        password_hash=pwd_hasher.hash(raw_password),
        nome=payload.nome,
        cognome=payload.cognome,
        cf=payload.cf,
        telefono=payload.telefono,
        data_nascita=payload.data_nascita.date() if payload.data_nascita else None,
        citta=payload.citta,
        indirizzo=payload.indirizzo,
        cap=payload.cap,
        paese=payload.paese,
    )

    db.add(user)
    db.flush()

    for role in roles:
        db.add(UtenteRuolo(utente_id=user.id, ruolo_id=role.id))

    db.commit()
    db.refresh(user)

    return CreatedUserResponse(user=user.username, psw=raw_password)


def update_password(
    db: Session,
    user: Utente,
    *,
    old_password: str,
    new_password: str,
) -> UpdateResponse:
    if not verify_password(old_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password errata",
        )
    if new_password is None or len(new_password.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password non compilata",
        )
    user.password_hash = hash_password(new_password)
    db.commit()
    db.refresh(user)
    return UpdateResponse(Result=1, update_timestamp=user.updated_at)


def update_profile(
    db: Session,
    user: Utente,
    payload: TutorSettingsUpdateRequest,
) -> UpdateResponse:
    ensure_unique_user_fields(
        db,
        email=payload.email,
        cf=payload.cf,
        user_id=user.id,
    )

    updates = payload.dict(exclude_unset=True)
    for key, value in updates.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return UpdateResponse(Result=1, update_timestamp=user.updated_at)