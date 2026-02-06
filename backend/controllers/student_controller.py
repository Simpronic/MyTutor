from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.db.base import get_db
from backend.model import Utente
from backend.schemas.student_controller_schemas import StudentCreateRequest, StudentResponse
from backend.security.dependencies import require_permission
import backend.services.student_service as student_service

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/createStudent", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentCreateRequest,
    user: Utente = Depends(require_permission("LESSON_CREATE")),
    db: Session = Depends(get_db),
) -> StudentResponse:
    return student_service.create_student(db, user, payload)