from __future__ import annotations

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.db.base import get_db
from backend.model import Utente
from backend.schemas.student_controller_schemas import (
    StudentCreateRequest,
    StudentResponse,
    StudentUpdateRequest,
    StudentUpdateResponse,
)
from backend.security.dependencies import require_permission
import backend.services.student_service as student_service

router = APIRouter(prefix="/students", tags=["students"])

@router.get("/getStudents", response_model=list[StudentResponse])
def list_students(
    user: Utente = Depends(require_permission("LESSON_READ")),
    db: Session = Depends(get_db),
) -> list[StudentResponse]:
    return student_service.list_students(db, user)


@router.get("/getStudent/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    user: Utente = Depends(require_permission("LESSON_READ")),
    db: Session = Depends(get_db),
) -> StudentResponse:
    return student_service.get_student(db, user, student_id)

@router.post("/createStudent", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(
    payload: StudentCreateRequest,
    user: Utente = Depends(require_permission("LESSON_CREATE")),
    db: Session = Depends(get_db),
) -> StudentResponse:
    return student_service.create_student(db, user, payload)

@router.patch("/updateStudent/{student_id}", response_model=StudentUpdateResponse)
def update_student(
    student_id: int,
    payload: StudentUpdateRequest,
    user: Utente = Depends(require_permission("LESSON_UPDATE")),
    db: Session = Depends(get_db),
) -> StudentUpdateResponse:
    return student_service.update_student(db, user, student_id, payload)


@router.patch("/toggleStudent/{student_id}", response_model=StudentUpdateResponse)
def toggle_student(
    student_id: int,
    user: Utente = Depends(require_permission("LESSON_UPDATE")),
    db: Session = Depends(get_db),
) -> StudentUpdateResponse:
    return student_service.toggle_student(db, user, student_id)


@router.delete("/deleteStudent/{student_id}", response_model=StudentUpdateResponse)
def delete_student(
    student_id: int,
    user: Utente = Depends(require_permission("LESSON_CANCEL")),
    db: Session = Depends(get_db),
) -> StudentUpdateResponse:
    return student_service.delete_student(db, user, student_id)