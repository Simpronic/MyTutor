from __future__ import annotations

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.model import Utente

from backend.schemas.auth_controller_schemas import PaeseResponse
from backend.model.paese import Paese
from typing import List


def ensure_unique_user_fields(
    db: Session,
    *,
    username: Optional[str] = None,
    email: Optional[str] = None,
    cf: Optional[str] = None,
    user_id: Optional[int] = None,
) -> None:
    if username:
        existing_user = db.query(Utente).filter(Utente.username == username).first()
        if existing_user and existing_user.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Username già in uso",
            )

    if email:
        existing_email = db.query(Utente).filter(Utente.email == email).first()
        if existing_email and existing_email.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email già in uso",
            )

    if cf:
        existing_cf = db.query(Utente).filter(Utente.cf == cf).first()
        if existing_cf and existing_cf.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Codice fiscale già in uso",
            )
        

def get_countries(db: Session) -> List[PaeseResponse]:
    paesi = (
            db.query(
                Paese.id,
                Paese.nome,
                Paese.iso2,
                Paese.iso3,
                Paese.iso_numeric,
            )
            .filter(Paese.attivo == 1)
            .all()
        )
    return [
        PaeseResponse(
            id=r.id,
            nome=r.nome,
            iso2=r.iso2,
            iso3=r.iso3,
            iso_numeric=r.iso_numeric,
        )
        for r in paesi
    ]