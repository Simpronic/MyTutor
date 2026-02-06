from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class LessonCreateRequest(BaseModel):
    student_id: int
    materia_code: str
    start_at: datetime
    end_at: datetime
    note: Optional[str] = None


class LessonUpdateRequest(BaseModel):
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    note: Optional[str] = None


class LessonStatusUpdateRequest(BaseModel):
    status: str = Field(..., min_length=1, max_length=50)
    reason: Optional[str] = None


class LessonResponse(BaseModel):
    id: int
    tutor_id: int
    student_id: int
    materia_id: int
    status: str
    start_at: datetime
    end_at: datetime
    note: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True