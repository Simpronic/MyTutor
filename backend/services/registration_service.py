from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.model import Ruolo, Utente, UtenteRuolo
from backend.schemas.registration_controller_schemas import (
    RegistrationRequest,
    RegistrationResponse,
)
from backend.security.password import hash_password
from backend.services.user_helpers import ensure_unique_user_fields


def register_user(db: Session, payload: RegistrationRequest) -> RegistrationResponse:
    ensure_unique_user_fields(
        db,
        username=payload.username,
        email=payload.email,
        cf=payload.cf,
    )

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
        attivo=1,
    )
    db.add(user)
    db.flush()

    link = UtenteRuolo(utente_id=user.id, ruolo_id=ruolo_tutor.id)
    db.add(link)
    db.commit()
    db.refresh(user)

    return RegistrationResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        ruolo=ruolo_tutor.nome,
    )