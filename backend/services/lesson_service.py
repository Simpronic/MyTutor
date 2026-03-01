from __future__ import annotations

from typing import List,Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import datetime,date
from backend.model import Lezione, LezionePartecipante, Materia, Studente, Utente
from backend.schemas.lesson_controller_schemas import (
    LessonCreateRequest,
    LessonResponse,
    LessonStatusUpdateRequest,
    LessonUpdateRequest,
    SubjectOptionResponse,
    LessonStudentInfo
)


def _to_lesson_response(lezione: Lezione) -> LessonResponse:
    students = [
        LessonStudentInfo(
            id=participant.studente.id,
            nome=participant.studente.nome,
            cognome=participant.studente.cognome,
    )
    for participant in lezione.partecipanti_link
]
    return LessonResponse(
        id=lezione.id,
        tutor_id=lezione.tutor_id,
        students=students,
        materia_id=lezione.materia_id,
        status=lezione.stato,
        data_inizio=lezione.data_inizio,
        data_fine=lezione.data_fine,
        note=lezione.note,
        created_at=lezione.created_at,
        updated_at=lezione.updated_at,
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

    student_ids = sorted(set(payload.student_ids or []))
    if not student_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Seleziona almeno uno studente",
        )
    materia_code = payload.materia_code.strip().upper()
    if not materia_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Materia non valida",
        )

    materia = db.query(Materia).filter(Materia.id == materia_code).one_or_none()
    if materia is None:
        materia = Materia(nome=materia_code)
        db.add(materia)
        db.flush()

    students = (
        db.query(Studente)
        .filter(Studente.tutor_id == user.id, Studente.id.in_(student_ids))
        .all()
    )
    if len(students) != len(student_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Uno o più studenti non trovati",
        )

    overlapping = (
        db.query(Lezione)
        .filter(
            Lezione.tutor_id == user.id,
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

    for student_id in student_ids:
        db.add(LezionePartecipante(lezione_id=lezione.id, studente_id=student_id))
    db.commit()
    db.refresh(lezione)
    return _to_lesson_response(lezione)

def list_subjects(
    db: Session
) -> List[SubjectOptionResponse]:
    subjects = (
        db.query(Materia)
        .all()
    )
    materie = [
        SubjectOptionResponse(code=subject.id, label=subject.nome)
        for subject in subjects
    ]
    return materie


def list_lessons(
    db: Session,
    user: Utente,
    start: Optional[date],
    end: Optional[date]
) -> List[LessonResponse]:
    query = db.query(Lezione).filter(Lezione.tutor_id == user.id)

    if start is not None and end is not None:
        if start > end:
            raise ValueError("Intervallo non valido: start > end")
        query = query.filter(Lezione.data_inizio >= start, Lezione.data_fine <= end)
    elif start is not None:
        query = query.filter(Lezione.data_inizio >= start)
    elif end is not None:
        query = query.filter(Lezione.data_fine <= end)
        query = query.filter(Lezione.data_fine <= end)

    lessons = query.order_by(Lezione.data_inizio.asc()).all()
    return [_to_lesson_response(lesson) for lesson in lessons]

def list_all_lessons(
        db:Session
) -> List[LessonResponse]:
    lessons = db.query(Lezione).order_by(Lezione.data_inizio.asc()).all()
    return [_to_lesson_response(lesson) for lesson in lessons]

def get_lesson(
    db: Session,
    user: Utente,
    lesson_id: int,
) -> LessonResponse:
    lesson = db.query(Lezione).filter(Lezione.id == lesson_id,
                                    Lezione.tutor_id == user.id
                                    ).one_or_none()
    if lesson is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lezione non trovata")
    return _to_lesson_response(lesson)


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