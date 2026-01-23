from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.orm import Session

from backend.db.base import get_db
from backend.model import Ruolo, Utente, UtenteRuolo

from backend.schemas.registration_controller_schemas import * 

from backend.security.password import(
    hash_password
)

router = APIRouter(prefix="/registration", tags=["registration"])

@router.post("/registerUser", response_model=RegistrationResponse, status_code=status.HTTP_201_CREATED)
def register_user(payload: RegistrationRequest, db: Session = Depends(get_db)) -> RegistrationResponse:
    existing_username = db.query(Utente).filter(Utente.username == payload.username).first()
    if existing_username:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username già in uso")

    existing_email = db.query(Utente).filter(Utente.email == payload.email).first()
    if existing_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email già in uso")

    if payload.cf:
        existing_cf = db.query(Utente).filter(Utente.cf == payload.cf).first()
        if existing_cf:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Codice fiscale già in uso")

    ruolo_tutor = db.query(Ruolo).filter(Ruolo.nome == "tutor").first()
    if not ruolo_tutor:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ruolo 'tutor' non configurato",
        )

    user = Utente(
        username=payload.username,
        email=payload.email,
        password_hash=hash_password(payload.password),
        nome=payload.nome,
        cognome=payload.cognome,
        cf=payload.cf,
        telefono=payload.telefono,
        data_nascita=payload.data_nascita,
        citta=payload.citta,
        indirizzo=payload.indirizzo,
        cap=payload.cap,
        paese=payload.paese,
        attivo=1
    )
    db.add(user)
    db.flush()

    link = UtenteRuolo(utente_id=user.id, ruolo_id=ruolo_tutor.id)
    db.add(link)
    db.commit()
    db.refresh(user)

    return RegistrationResponse(id=user.id, username=user.username, email=user.email, ruolo=ruolo_tutor.nome)