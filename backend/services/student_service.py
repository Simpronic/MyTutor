from __future__ import annotations

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.model import Studente, Utente
from backend.schemas.student_controller_schemas import StudentCreateRequest, StudentResponse


def create_student(
    db: Session,
    user: Utente,
    payload: StudentCreateRequest,
) -> StudentResponse:
    nome = payload.nome.strip()
    cognome = payload.cognome.strip()
    if not nome or not cognome:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nome e cognome sono obbligatori",
        )

    if payload.email:
        existing_email = (
            db.query(Studente)
            .filter(Studente.tutor_id == user.id, Studente.email == payload.email)
            .first()
        )
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email già in uso per questo tutor",
            )

    if payload.cf:
        existing_cf = (
            db.query(Studente)
            .filter(Studente.tutor_id == user.id, Studente.cf == payload.cf)
            .first()
        )
        if existing_cf:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Codice fiscale già in uso per questo tutor",
            )

    student = Studente(
        tutor_id=user.id,
        nome=nome,
        cognome=cognome,
        email=payload.email,
        telefono=payload.telefono,
        cf=payload.cf,
        data_nascita=payload.data_nascita,
        citta=payload.citta,
        indirizzo=payload.indirizzo,
        cap=payload.cap,
        paese=payload.paese,
        pagante_nome=payload.pagante_nome,
        pagante_cognome=payload.pagante_cognome,
        pagante_cf=payload.pagante_cf,
        pagante_email=payload.pagante_email,
        pagante_telefono=payload.pagante_telefono,
        pagante_indirizzo=payload.pagante_indirizzo
    )

    db.add(student)
    db.commit()
    db.refresh(student)
    return StudentResponse.model_validate(student)