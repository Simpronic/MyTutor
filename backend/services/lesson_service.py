from __future__ import annotations

from typing import List

from sqlalchemy.orm import Session

from backend.model import Utente,Lezione
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
    raise NotImplementedError


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