from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db.base import get_db
from backend.model import Utente
from backend.security.dependencies import get_current_user,require_permission
import backend.services.lesson_service as lesson_service
from backend.schemas.lesson_controller_schemas import (
    LessonCreateRequest,
    LessonResponse,
    LessonStatusUpdateRequest,
    LessonUpdateRequest,
)

router = APIRouter(prefix="/lessons", tags=["lessons"])

@router.post("/createLesson", response_model=LessonResponse)
def createLesson(
    payload: LessonCreateRequest,
    user:Utente = Depends(require_permission("LESSON_CREATE")),
    db: Session = Depends(get_db)  
) -> LessonResponse:
    return lesson_service.create_lesson(db,user,payload)

@router.get("user/getAllLessons", response_model=List[LessonResponse])
def createLesson(
    user:Utente = Depends(require_permission("LESSON_READ")),
    db: Session = Depends(get_db)  
) -> List[LessonResponse]:
    return lesson_service.list_lessons(db,user)

@router.get("/getAllLessons", response_model=List[LessonResponse])
def createLesson(
    _:Utente = Depends(require_permission("USER_CREATE")), #Impongo che debba avere USER_CREATE perche' solo un SYS admin puo' farlo 
    db: Session = Depends(get_db)  
) -> List[LessonResponse]:
    return lesson_service.list_all_lessons(db)

@router.get("/getLesson/{lesson_id}", response_model=LessonResponse)
def get_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    user: Utente = Depends(require_permission("LESSON_READ")),
) -> LessonResponse:
    return lesson_service.get_lesson(db,user,lesson_id)

@router.patch("updateLesson/{lesson_id}", response_model=LessonResponse)
def update_lesson(
    lesson_id: int,
    payload: LessonUpdateRequest,
    db: Session = Depends(get_db),
    user: Utente = Depends(require_permission("LESSON_UPDATE")),
) -> LessonResponse:
    return lesson_service.update_lesson(db,user,lesson_id,payload)


@router.patch("/{lesson_id}/status", response_model=LessonResponse)
def update_lesson_status(
    lesson_id: int,
    payload: LessonStatusUpdateRequest,
    db: Session = Depends(get_db),
    user: Utente = Depends(require_permission("LESSON_UPDATE")),
) -> LessonResponse:
    return lesson_service.update_lesson_status(db,user,lesson_id,payload)


@router.delete("/{lesson_id}")
def delete_lesson(
    lesson_id: int,
    db: Session = Depends(get_db),
    user: Utente = Depends(require_permission("LESSON_CANCEL")),
) -> dict:
    return lesson_service.delete_lesson(db,user,lesson_id)