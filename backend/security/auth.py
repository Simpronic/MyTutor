# backend/security/auth.py

from datetime import datetime, timedelta, timezone
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from backend.core.config import get_settings
from backend.db.base import get_db
from backend.model import Utente, Sessione

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

settings = get_settings()

SESSION_DURATION_MINUTES = settings.session_duration_minutes


def _utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


def create_session(db: Session, user: Utente) -> Sessione:
    existing = db.query(Sessione).filter(Sessione.utente_id == user.id).first()
    if existing:
        if existing.expires_at > _utc_now():
            refresh_session(db, existing)
            db.refresh(existing)
            return existing
        existing.token = secrets.token_urlsafe(32)
        existing.created_at = _utc_now()
        existing.last_seen_at = existing.created_at
        existing.expires_at = existing.created_at + timedelta(minutes=SESSION_DURATION_MINUTES)
        db.commit()
        db.refresh(existing)
        return existing

    token = secrets.token_urlsafe(32)
    expires_at = _utc_now() + timedelta(minutes=SESSION_DURATION_MINUTES)
    session = Sessione(token=token, utente_id=user.id,created_at=_utc_now(),expires_at=expires_at)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def refresh_session(db: Session, session: Sessione) -> None:
    session.last_seen_at = _utc_now()
    session.expires_at = session.last_seen_at + timedelta(minutes=SESSION_DURATION_MINUTES)
    db.commit()

def revoke_session(db: Session, token: str) -> bool:
    session = db.query(Sessione).filter(Sessione.token == token).first()
    if not session:
        return False
    db.delete(session)
    db.commit()
    return True

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Utente:
    session = db.query(Sessione).filter(Sessione.token == token,Sessione.expires_at >= datetime.now()).first()
    if not session:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    if session.expires_at <= _utc_now():
        db.delete(session)
        db.commit()
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Session expired")
    user = db.query(Utente).filter(Utente.id == session.utente_id, Utente.attivo == 1).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    refresh_session(db, session)
    return user
