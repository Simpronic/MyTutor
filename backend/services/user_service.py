from __future__ import annotations

import datetime
from typing import List

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.model import Ruolo, Utente, UtenteRuolo
from backend.schemas.userManagement_controller_schemas import (
    CreatedUserResponse,
    RolesResponse,
    TutorSettingsUpdateRequest,
    UpdateResponse,
    UserCreate,
    UserFullResponse,
    UserUpdateRequest,
)
from backend.security.password import hash_password, pwd_hasher, verify_password
from backend.services.user_helpers import ensure_unique_user_fields


def resetPsw(u_id:int, db:Session) -> UpdateResponse:
    user = db.query(Utente).filter(Utente.id == u_id).one_or_none()
    if(user == None): return UpdateResponse(Result=-1,update_timestamp=datetime.datetime.now())
    user.password_hash = hash_password("RESET_REQUIRED")
    db.commit()
    db.refresh(user)
    return UpdateResponse(Result=1,update_timestamp=user.updated_at)

def getAllUsers(u:Utente,db:Session) -> List[UserFullResponse]:
    return db.query(Utente).filter(Utente.id != u.id)
    
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

    #raw_password = secrets.token_urlsafe(12)
    user = Utente(
        username=payload.username,
        email=payload.email,
        password_hash=pwd_hasher.hash(payload.password),
        nome=payload.nome,
        cognome=payload.cognome,
        cf=payload.cf,
        telefono=payload.telefono,
        data_nascita=payload.data_nascita.date() if payload.data_nascita else None,
        iban=payload.iban,
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

    return CreatedUserResponse(user=user.username)


def updatePassword(
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

def toggleUser(
        db: Session,
        user_id: int
) -> UpdateResponse:
    user = db.query(Utente).filter(Utente.id == user_id).first()
    if(user == None): return UpdateResponse(Result=-1,update_timestamp=datetime.datetime.now())
    user.attivo = 1 if user.attivo == 0 else 0
    db.commit()
    db.refresh(user)
    return UpdateResponse(Result=1,update_timestamp=user.updated_at)

def getUserInfos(
        db: Session,
        user_id:int 
) -> UserFullResponse:
    return db.query(Utente).filter(Utente.id == user_id).first()
    

def deleteUser(
        db: Session,
        user_id:int
) -> UpdateResponse:
    db.query(Utente).filter(Utente.id == user_id).delete()
    db.commit()
    return UpdateResponse(Result=1,update_timestamp=datetime.datetime.now())
    
def updateProfile(
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

def updateUser(
    db: Session,
    user_id: int,
    payload: UserUpdateRequest,
) -> UpdateResponse:
    user = db.query(Utente).filter(Utente.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utente non trovato",
        )

    ensure_unique_user_fields(
        db,
        username=payload.username,
        email=payload.email,
        cf=payload.cf,
        user_id=user.id,
    )

    updates = payload.dict(exclude_unset=True, exclude={"ruoli"})
    for key, value in updates.items():
        setattr(user, key, value)

    if payload.ruoli is not None:
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

        db.query(UtenteRuolo).filter(UtenteRuolo.utente_id == user.id).delete()
        for role in roles:
            db.add(UtenteRuolo(utente_id=user.id, ruolo_id=role.id))

    db.commit()
    db.refresh(user)
    return UpdateResponse(Result=1, update_timestamp=user.updated_at)