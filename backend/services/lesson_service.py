from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from backend.model import Lezione, LezionePartecipante, Materia, Studente, Utente
from backend.schemas.lesson_controller_schemas import (
    LessonCreateRequest,
    LessonResponse,
    LessonStatusUpdateRequest,
    LessonUpdateRequest,
)


def create_lesson(
    db: Session,
    user: Utente,
    payload: LessonCreateRequest,
) -> LessonResponse:
    if payload.start_at >= payload.end_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Intervallo orario non valido",
        )

    materia_code = payload.materia_code.strip().upper()
    if not materia_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Materia non valida",
        )

    materia = db.query(Materia).filter(Materia.nome == materia_code).one_or_none()
    if materia is None:
        materia = Materia(nome=materia_code)
        db.add(materia)
        db.flush()

    student = (
        db.query(Studente)
        .filter(Studente.id == payload.student_id, Studente.tutor_id == payload.tutor_id)
        .one_or_none()
    )
    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Studente non trovato",
        )

    overlapping = (
        db.query(Lezione)
        .filter(
            Lezione.tutor_id == payload.tutor_id,
            Lezione.data_inizio < payload.end_at,
            Lezione.data_fine > payload.start_at,
        )
        .first()
    )
    if overlapping is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Esiste già una lezione in questo intervallo",
        )

    lezione = Lezione(
        tutor_id=user.id,
        materia_id=materia.id,
        data_inizio=payload.start_at,
        data_fine=payload.end_at,
        note=payload.note,
    )
    db.add(lezione)
    db.flush()

    db.add(LezionePartecipante(lezione_id=lezione.id, studente_id=student.id))
    db.commit()
    db.refresh(lezione)
    return LessonResponse.model_validate(lezione)


def list_lessons(
    db: Session,
    user: Utente,
) -> List[LessonResponse]:
    raise NotImplementedError

def list_all_lessons(
        db:Session
) -> List[LessonResponse]:
    raise NotImplementedError

def get_lesson(
    db: Session,
    user: Utente,
    lesson_id: int,
) -> LessonResponse:
    raise NotImplementedError


def update_lesson(
    db: Session,
    user: Utente,
    lesson_id: int,
    payload: LessonUpdateRequest,
) -> LessonResponse:
    raise NotImplementedError


def update_lesson_status(
    db: Session,
    user: Utente,
    lesson_id: int,
    payload: LessonStatusUpdateRequest,
) -> LessonResponse:
    raise NotImplementedError


def delete_lesson(
    db: Session,
    user: Utente,
    lesson_id: int,
) -> dict:
    raise NotImplementedError