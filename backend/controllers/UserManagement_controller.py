from __future__ import annotations

from datetime import datetime
import secrets
from typing import List, Optional

from argon2 import PasswordHasher
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.db.base import get_db
from backend.model import Ruolo, Utente, UtenteRuolo
from backend.security.dependencies import require_permission,get_current_user

router = APIRouter(prefix="/userManagement", tags=["userManagement"])

pwd_hasher = PasswordHasher()


class RuoloCreate(BaseModel):
    nome: str

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, max_length=64)
    email: str = Field(..., min_length=1, max_length=254)
    nome: str = Field(..., min_length=1, max_length=100)
    cognome: str = Field(..., min_length=1, max_length=100)
    cf: Optional[str] = Field(None, max_length=16)
    telefono: Optional[str] = Field(None, max_length=30)
    data_nascita: Optional[datetime] = None
    citta: Optional[str] = Field(None, max_length=120)
    indirizzo: Optional[str] = Field(None, max_length=255)
    cap: Optional[str] = Field(None, max_length=10)
    paese: Optional[str] = Field(None, max_length=2)
    ruoli: List[RuoloCreate] = Field(default_factory=list)

    class Config:
        from_attributes = True


class CreatedUserResponse(BaseModel):
    user: str
    psw: str


class RolesResponse(BaseModel):
    id: int
    nome: str
    descrizione: str

    class Config:
        from_attributes = True

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