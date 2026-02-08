from __future__ import annotations


import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.model import Studente, Utente
from backend.schemas.student_controller_schemas import (
    StudentCreateRequest,
    StudentResponse,
    StudentUpdateRequest,
    StudentUpdateResponse,
)


def _ensure_unique_student_fields(
    db: Session,
    tutor_id: int,
    *,
    email: str | None = None,
    cf: str | None = None,
    student_id: int | None = None,
) -> None:
    if email:
        query = db.query(Studente).filter(Studente.tutor_id == tutor_id, Studente.email == email)
        if student_id is not None:
            query = query.filter(Studente.id != student_id)
        if query.first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email già in uso per questo tutor",
            )

    if cf:
        query = db.query(Studente).filter(Studente.tutor_id == tutor_id, Studente.cf == cf)
        if student_id is not None:
            query = query.filter(Studente.id != student_id)
        if query.first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Codice fiscale già in uso per questo tutor",
            )


def _get_student_for_tutor(db: Session, tutor_id: int, student_id: int) -> Studente:
    student = (
        db.query(Studente)
        .filter(Studente.id == student_id, Studente.tutor_id == tutor_id)
        .first()
    )
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Studente non trovato",
        )
    return student


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
    _ensure_unique_student_fields(
        db,
        user.id,
        email=payload.email,
        cf=payload.cf,
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



def list_students(db: Session, user: Utente) -> list[StudentResponse]:
    return (
        db.query(Studente)
        .filter(Studente.tutor_id == user.id)
        .order_by(Studente.cognome, Studente.nome)
        .all()
    )


def get_student(db: Session, user: Utente, student_id: int) -> StudentResponse:
    student = _get_student_for_tutor(db, user.id, student_id)
    return StudentResponse.model_validate(student)


def update_student(
    db: Session,
    user: Utente,
    student_id: int,
    payload: StudentUpdateRequest,
) -> StudentUpdateResponse:
    student = _get_student_for_tutor(db, user.id, student_id)

    _ensure_unique_student_fields(
        db,
        user.id,
        email=payload.email,
        cf=payload.cf,
        student_id=student.id,
    )

    updates = payload.model_dump(exclude_unset=True)
    if "nome" in updates and updates["nome"] is not None:
        updates["nome"] = updates["nome"].strip()
    if "cognome" in updates and updates["cognome"] is not None:
        updates["cognome"] = updates["cognome"].strip()

    for key, value in updates.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)
    return StudentUpdateResponse(Result=1, update_timestamp=student.updated_at)


def toggle_student(
    db: Session,
    user: Utente,
    student_id: int,
) -> StudentUpdateResponse:
    student = _get_student_for_tutor(db, user.id, student_id)
    student.attivo = not bool(student.attivo)
    db.commit()
    db.refresh(student)
    return StudentUpdateResponse(Result=1, update_timestamp=student.updated_at)


def delete_student(
    db: Session,
    user: Utente,
    student_id: int,
) -> StudentUpdateResponse:
    student = _get_student_for_tutor(db, user.id, student_id)
    db.delete(student)
    db.commit()
    return StudentUpdateResponse(Result=1, update_timestamp=datetime.datetime.now())
