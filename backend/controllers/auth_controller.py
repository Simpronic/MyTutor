from __future__ import annotations

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

from backend.db.base import get_db
from backend.model import Utente


router = APIRouter(prefix="/auth", tags=["auth"])

# Argon2 hasher (config di default sicura)
pwd_hasher = PasswordHasher()


# ----------- SCHEMI Pydantic -----------

class LoginRequest(BaseModel):
    identifier: str = Field(..., min_length=1, max_length=254, description="Username oppure email")
    password: str = Field(..., min_length=1, max_length=255)


class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    nome: str
    cognome: str
    attivo: bool

    class Config:
        from_attributes = True


class LoginResponse(BaseModel):
    user: UserPublic


# ----------- UTILS PASSWORD -----------

def hash_password(plain_password: str) -> str:
    """
    Crea hash Argon2 da password in chiaro.
    (Usalo in fase di registrazione o seed DB)
    """
    return pwd_hasher.hash(plain_password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Verifica password in chiaro contro hash Argon2.
    """
    print(hash_password("123"))
    try:
        return pwd_hasher.verify(password_hash, plain_password)
    except VerifyMismatchError:
        return False
    except Exception:
        # hash corrotto o formato sconosciuto
        return False


def is_email(s: str) -> bool:
    return "@" in s and "." in s


# ----------- ENDPOINT LOGIN -----------

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    identifier = payload.identifier.strip()

    q = db.query(Utente)
    if is_email(identifier):
        user = q.filter(Utente.email == identifier).first()
    else:
        user = q.filter(Utente.username == identifier).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenziali non valide",
        )

    if not user.attivo:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Utente disattivato",
        )

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenziali non valide",
        )

    # aggiorna last_login_at
    user.last_login_at = datetime.now(timezone.utc).replace(tzinfo=None)
    db.commit()
    db.refresh(user)

    return LoginResponse(user=user)
