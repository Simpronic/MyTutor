from __future__ import annotations

import secrets
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from backend.db.base import get_db
from backend.model import Ruolo, Utente, UtenteRuolo
from backend.security.dependencies import require_permission,get_current_user
from backend.security.password import pwd_hasher

from backend.schemas.UserManagement_controller_schemas import *
from backend.security.password import (verify_password,hash_password)


router = APIRouter(prefix="/userManagement", tags=["userManagement"])

@router.get("/roles",response_model=List[RolesResponse])
def getAllRoles(
    db: Session = Depends(get_db),
    _: Utente = Depends(get_current_user)
) -> List[RolesResponse]:
    return db.query(Ruolo).all()

@router.post("/addUser", response_model=CreatedUserResponse)
def add_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
    _: Utente = Depends(require_permission("user.create")),
) -> CreatedUserResponse:
    existing_user = db.query(Utente).filter(Utente.username == payload.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username già in uso",
        )

    existing_email = db.query(Utente).filter(Utente.email == payload.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email già in uso",
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
    if(not verify_password(payload.old_password,user.password_hash)):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Password errata"
        )
    if(payload.new_password is None or len(payload.new_password.strip())== 0):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password non compilata"
        )
    user.password_hash = hash_password(payload.new_password)
    db.commit()
    db.refresh(user)
    return UpdateResponse(Result=1,update_timestamp=user.updated_at )


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
    if payload.email and payload.email != user.email:
        existing_email = db.query(Utente).filter(Utente.email == payload.email).first()
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email già in uso",
            )
        user.email = payload.email

    if payload.cf and payload.cf != user.cf:
        existing_cf = db.query(Utente).filter(Utente.cf == payload.cf).first()
        if existing_cf:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Codice fiscale già in uso",
            )
        user.cf = payload.cf

    if payload.nome is not None:
        user.nome = payload.nome
    if payload.cognome is not None:
        user.cognome = payload.cognome
    if payload.telefono is not None:
        user.telefono = payload.telefono
    if payload.data_nascita is not None:
        user.data_nascita = payload.data_nascita
    if payload.citta is not None:
        user.citta = payload.citta
    if payload.indirizzo is not None:
        user.indirizzo = payload.indirizzo
    if payload.cap is not None:
        user.cap = payload.cap
    if payload.paese is not None:
        user.paese = payload.paese

    db.commit()
    db.refresh(user)
    return UpdateResponse(Result=1,update_timestamp=user.updated_at)